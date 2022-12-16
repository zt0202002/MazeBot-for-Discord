async def slash2(ctx):
# await interaction.response.send_message(f"I am working! I was made with Discord.py!", ephemeral = True) 
    await ctx.defer(ephemeral=True)
    await ctx.reply('I am working! I was made with Discord.py!')