from discord.ext import commands


async def send_secret_message(ctx: commands.Context, message: str):
    if ctx.interaction:
        return await ctx.interaction.response.send_message(message)
    else:
        return await ctx.author.send(message)
