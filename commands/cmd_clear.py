async def clear(ctx, amount):
    await ctx.channel.purge(limit=amount + 1)
    # await msg.send("Messages have been cleared")