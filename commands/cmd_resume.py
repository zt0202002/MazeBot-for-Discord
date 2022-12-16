import discord
from discord.utils import get

async def resume(ctx, bot):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        embedVar = discord.Embed(title=f'歌曲又开始播放啦！', description=f'', color=0x487B60)
        await ctx.send(embed=embedVar)

async def pause(ctx, bot):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        embedVar = discord.Embed(title=f'歌曲被暂停啦！', description=f'', color=0x487B60)
        await ctx.send(embed=embedVar)