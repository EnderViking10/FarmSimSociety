from discord.ext import commands
from utils.permissions import has_any_role
import asyncio
import json

from packages.database import UserRepository


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self._last_member = None

    @commands.hybrid_command(name="sync_commands", description="Sync commands")
    @has_any_role("Owner", "Co Owner")
    async def sync_commands(self, ctx: commands.Context):
        """Sync bot commands with Discord."""
        await self.bot.tree.sync()
        response_message = "Commands have been synced"
        if ctx.interaction:
            await ctx.interaction.response.send_message(response_message)
        else:
            await ctx.reply(response_message)

    @sync_commands.error
    async def sync_commands_error(self, ctx: commands.Context, error):
        """Handles errors for sync_commands."""
        if isinstance(error, commands.CheckFailure):
            response_message = "You must have all required roles to use this command."
            if ctx.interaction:
                await ctx.interaction.response.send_message(response_message)
            else:
                await ctx.reply(response_message)

    async def send_to_clients(self, payload):
        """Sends a JSON payload to all connected WebSocket clients."""
        if self.connected_clients:
            await asyncio.gather(*(client.send(json.dumps(payload)) for client in self.connected_clients))
        else:
            raise RuntimeError("No FS25 servers connected.")

    @commands.hybrid_command(name="add_money", description="Add money to a farm in FS25")
    @has_any_role("Owner", "Co Owner")
    async def add_money(self, ctx: commands.Context, user: discord.User, amount: int):
        """Adds money to a specific farm."""
        if amount <= 0:
            await ctx.reply("Amount must be greater than 0!")
            return

        UserRepository.add_money(self.bot.session, user.id, amount)

        try:
            await ctx.reply(f"Added {amount} to {user.name}")
        except RuntimeError as e:
            await ctx.reply(str(e))

    @commands.hybrid_command(name="remove_money", description="Remove money from a farm in FS25")
    @has_any_role("Owner", "Co Owner")
    async def remove_money(self, ctx: commands.Context, server_id: int, farm_id: int, amount: int):
        """Removes money from a specific farm."""
        if amount <= 0:
            await ctx.reply("Amount must be greater than 0!")
            return



        try:
            await ctx.reply(f"Requested to remove ${amount} from Farm {farm_id}.")
        except RuntimeError as e:
            await ctx.reply(str(e))


async def setup(bot):
    """Loads the Admin cog into the bot."""
    cog = Admin(bot)

    # Retrieve WebSocket connections from WebSocketHandler cog
    websocket_handler = bot.get_cog("WebSocketHandler")
    if websocket_handler:
        cog.connected_clients = websocket_handler.connected_clients

    await bot.add_cog(cog)
