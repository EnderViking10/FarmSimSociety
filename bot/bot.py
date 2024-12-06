import os

import discord
from database import Database
from discord.ext import commands
from dotenv import load_dotenv

from utils.logger import logger

# Load environment variables
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("COMMAND_PREFIX", "!")
WEBSOCKET_HOST = os.getenv("WEBSOCKET_HOST", "0.0.0.0")
WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", 8765))
DATABASE_URL = os.getenv("DATABASE_URL", 'sqlite:///' + os.path.join(basedir, '../data/data.db'))

# Intents
intents = discord.Intents.all()
intents.message_content = True


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = Database(DATABASE_URL)
        self.session = self.db.get_session()

    # Bot Events
    async def on_ready(self):
        """Runs when the bot is ready."""
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

        # Load all cogs in the cogs/ folder
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                cog_name = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(cog_name)
                    logger.info(f"Loaded {cog_name}")
                except Exception as e:
                    logger.error(f"Failed to load cog {cog_name}: {e}")

    async def on_command(self, ctx):
        """Logs when a command is run."""
        logger.info(
            f"{ctx.author} : {ctx.author.id} ran {ctx.command} in channel '{ctx.channel}'."
        )

    async def on_command_error(self, ctx, error):
        """Handles errors for commands."""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found. Type `!help` for a list of commands.")
        else:
            logger.error(f"Error in command {ctx.command}: {error}")


def main():
    bot = Bot(command_prefix=PREFIX, intents=intents)
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
