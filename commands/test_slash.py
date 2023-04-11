import discord
async def slash2(ctx):
# await interaction.response.send_message(f"I am working! I was made with Discord.py!", ephemeral = True) 
    await ctx.defer(ephemeral=True)
    await ctx.reply('I am working! I was made with Discord.py!')

    embed1 = discord.embeds.Embed(title="Scorch Gorge", description="")
    embed2 = discord.embeds.Embed(title="Mincemeat Metalworks", description="")

    embed1.set_image(url="https://splatoon3.ink/assets/splatnet/v1/stage_img/icon/low_resolution/35f9ca08ccc2bf759774ab2cb886567c117b9287875ca92fb590c1294ddcdc1e_1.png")
    embed2.set_image(url="https://splatoon3.ink/assets/splatnet/v1/stage_img/icon/low_resolution/de1f212e9ff0648f36cd3b8e0917ef36b3bd51445159297dcb948f34a09f2f05_1.png")

    await ctx.send(embeds=[embed1, embed2])