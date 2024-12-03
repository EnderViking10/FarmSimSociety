import discord
from discord.ext import commands
from utils.database import Bank, get_db
from utils.fssapi import FSSAPI


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self._last_member = None
        self.fss_api = FSSAPI("http://192.168.1.207:8000")  # FS25 Server API base URL

    @commands.hybrid_command(name="bank", description="The bank command")
    async def bank(self, ctx: commands.Context):
        """Check your bank balance."""
        member = ctx.author
        bank_account = Bank.get_bank(next(get_db()), member.id)

        if bank_account is None:
            message = "You do not have a bank account in our system."
        else:
            message = f"Your balance is {bank_account.balance}"

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
        db = next(get_db())
        author = ctx.author

        # Retrieve bank accounts for sender and recipient
        author_bank = Bank.get_bank(db, author.id)
        user_bank = Bank.get_bank(db, user.id)

        if user_bank is None:
            message = f"User {user.name} is not in the database."
        elif author_bank.balance < amount:
            message = "You have insufficient funds."
        else:
            # Process the transfer
            user_bank.balance += amount
            author_bank.balance -= amount
            db.commit()
            message = f"{amount} has been transferred to {user.name}."

        db.close()

        if ctx.interaction:
            await ctx.interaction.response.send_message(message, ephemeral=True)
        else:
            await author.send(message)

    @transfer.command(name="server", description="Transfer money to a farm on a server")
    async def server(self, ctx: commands.Context, server: int, farm_name: str, amount: int):
        """Transfer money to a server's farm."""
        db = next(get_db())
        author = ctx.author
        author_bank = Bank.get_bank(db, author.id)

        if author_bank.balance < amount:
            message = "You have insufficient funds."
        else:
            # Deduct money from user's bank
            author_bank.balance -= amount
            db.commit()

            # Send command to FS25 server
            try:
                self.fss_api.send_command(
                    "add_money",
                    {
                        "farm_name": farm_name,
                        "amount": amount,
                        "server_id": server,  # Add server ID to the payload
                    },
                )
                message = f"{amount} has been transferred to farm '{farm_name}' on server {server}."
            except Exception as e:
                message = f"Failed to process transfer: {str(e)}"

        db.close()

        if ctx.interaction:
            await ctx.interaction.response.send_message(message, ephemeral=True)
        else:
            await author.send(message)


async def setup(bot):
    """Sets up the Economy cog."""
    await bot.add_cog(Economy(bot))
