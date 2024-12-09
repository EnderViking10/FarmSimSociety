from discord.ext import commands

from utils import send_secret_message


class Contracts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="contract")
    async def contract(self, ctx):
        await send_secret_message(ctx, message="You must use a subcommand")

    @contract.command(name="add")
    async def add_contract(self, ctx: commands.Context, title: str, description: str, price: int):




async def setup(bot):
    """Sets up the Economy cog."""
    await bot.add_cog(Contracts(bot))
