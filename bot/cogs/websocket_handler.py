import discord
from discord.ext import commands

class WebSocketHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connected_clients = set()

async def setup(bot):
    await bot.add_cog(WebSocketHandler(bot))
