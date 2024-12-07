import discord
from database import UserRepository, ServerRepository
from database.repository import PropertyRepository
from discord.ext import commands

from utils.permissions import has_any_role


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
    async def remove_money(self, ctx: commands.Context, user: discord.User, amount: int):
        """Removes money from a specific farm."""
        if amount <= 0:
            await ctx.reply("Amount must be greater than 0!")
            return

        try:
            await ctx.reply(f"Removed {amount} from {user.name}")
        except RuntimeError as e:
            await ctx.reply(str(e))

    @commands.hybrid_group(name="property", description="Deals with property")
    async def property_group(self, ctx: commands.Context):
        pass

    @property_group.command(name="add", description="Add a property")
    @has_any_role("Owner", "Co Owner")
    async def add_property(self, ctx: commands.Context, server_id: int, property_number: int, image_path: str,
                           size: int, price: int):
        """Adds a property to a specific farm."""
        if property_number < 0:
            return await ctx.reply("Property ID must be greater than 0!")

        server = ServerRepository.get_server_by_id(self.bot.session, server_id)
        if server is None:
            return await ctx.reply("Server ID doesn't exist!")

        property = PropertyRepository.get_property(self.bot.session, server_id, property_number)
        if property:
            return await ctx.reply("Property already exists!")

        property = PropertyRepository.create_property(self.bot.session, server_id=server_id,
                                                      property_number=property_number,
                                                      image=image_path, size=size, price=price)

        return await ctx.send("Property added!")

    @commands.hybrid_group(name="server", description="Deals with server")
    async def server_group(self, ctx: commands.Context):
        pass

    @server_group.command(name="add", description="Add a server")
    @has_any_role("Owner", "Co Owner")
    async def add_server(self, ctx: commands.Context, name: str, map: str, ip: str = None):
        server = ServerRepository.create_server(self.bot.session, ip=ip, name=name, map=map)

        return await ctx.send(f"{server.id} is the servers number")

    @commands.command(name="initdb", description="Initialize database")
    @has_any_role("Owner", "Co Owner")
    async def init_db(self, ctx: commands.Context):
        """Initializes the database."""
        members = ctx.guild.members
        for member in members:
            if member.bot:
                continue
            if UserRepository.get_user_by_discord_id(self.bot.session, member.id):
                continue
            UserRepository.create_user(self.bot.session, username=member.name, discord_id=member.id)

        await ctx.reply("Database initialized!")


async def setup(bot):
    """Loads the Admin cog into the bot."""
    cog = Admin(bot)

    await bot.add_cog(cog)
