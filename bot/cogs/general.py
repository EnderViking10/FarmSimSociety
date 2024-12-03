import asyncio

import discord
from discord import Member, Guild
from discord.ext import commands
import json

from utils.database import get_db, User, add_user


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.connected_clients = set()  # WebSocket connections

    # Event Listener: On Member Join
    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        """Sends a welcome message when a user joins the server."""
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Welcome {member.mention}!")

        # Adds the user to the database
        add_user(member)

    # Event Listener: On Bot Added to a Guild
    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        """Handles when the bot joins a new guild."""
        members = guild.members
        for member in members:
            if member.bot:
                continue
            if User.get_user(next(get_db()), member.id):
                continue
            add_user(member)

    # Event Listener: On User Update
    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        """Updates the database if a user changes their username."""
        if before.name == after.name:
            return
        User.update_username(next(get_db()), before.id, after.name)

    # WebSocket Event Listener
    @commands.Cog.listener()
    async def on_websocket_message(self, message):
        """Processes WebSocket messages from FS25 servers."""
        data = json.loads(message)

        # Handle in-game chat messages
        if data["event"] == "chat_message":
            server_id = data["server_id"]
            player_name = data["player_name"]
            chat_message = data["message"]

            # Replace with your Discord channel ID mapped to the FS25 server_id
            channel_id = 123456789012345678  # Example channel ID
            channel = self.bot.get_channel(channel_id)
            if channel:
                await channel.send(f"**{player_name}:** {chat_message}")

    # Sync Discord Messages to FS25
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Forwards Discord messages to the FS25 server."""
        if message.author.bot:
            return

        # Replace with your logic to map server_id and channel_id
        server_id = "your_unique_server_id"
        channel_id = 123456789012345678  # Example channel ID

        # Check if the message is in the linked FS25 channel
        if message.channel.id == channel_id:
            payload = {
                "event": "discord_message",
                "server_id": server_id,
                "username": message.author.name,
                "message": message.content,
            }
            if self.connected_clients:
                await asyncio.gather(*(client.send(json.dumps(payload)) for client in self.connected_clients))
            else:
                await message.channel.send("No FS25 servers connected to receive this message.")

async def setup(bot):
    """Loads the General cog into the bot."""
    cog = General(bot)

    # Retrieve WebSocket connections from WebSocketHandler cog
    websocket_handler = bot.get_cog("WebSocketHandler")
    if websocket_handler:
        cog.connected_clients = websocket_handler.connected_clients

    await bot.add_cog(cog)
