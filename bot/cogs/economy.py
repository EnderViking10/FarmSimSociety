import discord
from discord.ext import commands
from database import UserRepository


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self._last_member = None

    @commands.hybrid_command(name="bank", description="The bank command")
    async def bank(self, ctx: commands.Context):
        """Check your bank balance."""
        member = ctx.author
        user = UserRepository.get_user_by_discord_id(self.bot.session, member.id)

        message = f"Your balance is {user.balance}"

        if ctx.interaction:
            await ctx.interaction.response.send_message(message, ephemeral=True)
        else:
            await ctx.author.send(message)

    @commands.hybrid_group(name="transfer", description="Transfer money")
    async def transfer(self, ctx: commands.Context):
        """Base command for transfer operations."""
        if ctx.interaction:
            await ctx.interaction.response.send_message("Use a subcommand to transfer money", ephemeral=True)
        else:
            await ctx.reply("Use a subcommand to transfer money")

    @transfer.command(name="player", description="Transfer money to another player")
    async def player(self, ctx: commands.Context, user: discord.User, amount: int):
        """Transfer money to another player."""
        _author = UserRepository.get_user_by_discord_id(self.bot.session, ctx.author.id)
        _user = UserRepository.get_user_by_discord_id(self.bot.session, user.id)

        # Retrieve bank accounts for sender and recipient

        if _user is None:
            message = f"User {user.name} is not in the database."
        elif _author.balance < amount:
            message = "You have insufficient funds."
        else:
            # Process the transfer
            UserRepository.add_money(self.bot.session, _user.id, amount)
            UserRepository.remove_money(self.bot.session, _author.id, amount)
            message = f"{amount} has been transferred to {user.name}."

        if ctx.interaction:
            await ctx.interaction.response.send_message(message, ephemeral=True)
        else:
            await _author.send(message)

async def setup(bot):
    """Sets up the Economy cog."""
    await bot.add_cog(Economy(bot))
