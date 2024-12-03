import os
import asyncio
import threading

import discord
from discord.ext import commands
from dotenv import load_dotenv
import websockets

from utils.database import init_db
from utils.logger import logger

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("COMMAND_PREFIX", "!")
WEBSOCKET_HOST = os.getenv("WEBSOCKET_HOST", "0.0.0.0")
WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", 8765))

# Intents
intents = discord.Intents.all()
intents.message_content = True

# Initialize the bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# WebSocket connections
connected_clients = set()


async def websocket_handler(websocket, path):
    """Handles incoming WebSocket connections from FS25 servers."""
    logger.info("FS25 server connected")
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            logger.info(f"WebSocket message received: {message}")
            # Dispatch a custom event for cogs to handle
            await bot.dispatch("websocket_message", message)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)


async def start_websocket_server():
    """Starts the WebSocket server."""
    server = await websockets.serve(websocket_handler, WEBSOCKET_HOST, WEBSOCKET_PORT)
    logger.info(f"WebSocket server running on ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
    await server.wait_closed()


def websocket_server_thread():
    """Runs the WebSocket server in a separate thread."""
    asyncio.run(start_websocket_server())


# Bot Events
@bot.event
async def on_ready():
    """Runs when the bot is ready."""
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")

    # Initialize the database
    init_db()
    logger.info("Database successfully initialized")

    # Load all cogs in the cogs/ folder
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                logger.info(f"Loaded {cog_name}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog_name}: {e}")


@bot.event
async def on_command(ctx):
    """Logs when a command is run."""
    logger.info(
        f"{ctx.author} : {ctx.author.id} ran {ctx.command} in channel '{ctx.channel}'."
    )


@bot.event
async def on_command_error(ctx, error):
    """Handles errors for commands."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Type `!help` for a list of commands.")
    else:
        logger.error(f"Error in command {ctx.command}: {error}")


def main():
    # Start the WebSocket server
    websocket_thread = threading.Thread(target=websocket_server_thread, daemon=True)
    websocket_thread.start()

    # Run the bot
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
