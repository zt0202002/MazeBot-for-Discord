from datetime import datetime
async def report(ctx, message, bot):
    with open("report.txt", "a+") as f:
        f.write(f"[{datetime.now()}] {ctx.author} reported: {message}\n")
    # await channel.send(f"{ctx.author} reported: {message}")
    await ctx.send(f"Bug reported at {datetime.now()}")