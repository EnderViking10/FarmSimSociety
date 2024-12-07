import asyncio

import discord
from database import UserRepository
from discord import Member, Guild
from discord.ext import commands
import json


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # Event Listener: On Member Join
    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        """Sends a welcome message when a user joins the server."""
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Welcome {member.mention}!")

        # Adds the user to the database
        UserRepository.create_user(self.bot.session, username=member.name, discord_id=member.id)

    # Event Listener: On Bot Added to a Guild
    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        """Handles when the bot joins a new guild."""
        members = guild.members
        for member in members:
            if member.bot:
                continue
            if UserRepository.get_user_by_discord_id(self.bot.session, member.id):
                continue
            UserRepository.create_user(self.bot.session, username=member.name, display_name=member.display_name, discord_id=member.id)

    # Event Listener: On User Update
    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        """Updates the database if a user changes their username."""
        if before.name == after.name:
            return
        UserRepository.update_username(self.bot.session, before.id, after.name)


async def setup(bot):
    """Loads the General cog into the bot."""
    await bot.add_cog(General(bot))
