import os
from datetime import timedelta, datetime

import discord
from database import AuctionRepository, UserRepository
from database.repository import PropertyRepository, ServerRepository
from discord.ext import commands
from discord.ui import Button, View

from utils import send_secret_message


class Auction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name='auction')
    async def auction(self, ctx):
        button = Button(label="Click me!", style=discord.ButtonStyle.green)

        async def button_callback(interaction):
            await interaction.response.send_message("Button clicked!")

        button.callback = button_callback

        view = View()
        view.add_item(button)

        await ctx.send("Here's a button!", view=view)

    @auction.command(name="new", description="Create a new auction")
    async def new_auction(self, ctx: commands.Context, server_id: int, property_id: int, end_time: int,
                          cost: int = None):
        user = UserRepository.get_user_by_discord_id(self.bot.session, ctx.author.id)
        property = PropertyRepository.get_property(self.bot.session, server_id, property_id)

        if property is None:
            return await ctx.send("That property doesn't exist")

        if not user.admin:
            if user.discord_id != property.user_id:
                return await ctx.send("You don't own this property")

        if end_time is None:
            end_time = 24

        end_time = datetime.now() + timedelta(hours=end_time)
        if cost is None:
            cost = property.price
        auction = AuctionRepository.create_auction(self.bot.session, server_id, property_id, cost, end_time)

        with open(f'{os.path.dirname(__file__)}\\..\\..\\data\\images\\{property.image}', 'rb') as f:
            image = discord.File(f)

        embed_dict = {
            'title': 'Auction',
            'description': 'Land auction',
            'color': 2,
            'fields': [
                {'name': 'Server', 'value': property.server_id},
                {'name': 'Property', 'value': property.id},
                {'name': 'Current Bid', 'value': auction.cost},
                {'name': 'NPC Price', 'value': property.price},
                {'name': 'End Time', 'value': auction.timeout},
            ]
        }

        embed = discord.Embed().from_dict(embed_dict)
        await ctx.guild.get_channel(int(os.getenv('AUCTION_CHANNEL'))).send(embed=embed)


async def setup(bot):
    """Sets up the Economy cog."""
    await bot.add_cog(Auction(bot))
