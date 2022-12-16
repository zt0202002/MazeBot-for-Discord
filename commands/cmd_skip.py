from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from help_functions.help_queue import *

async def skipall(ctx, bot):
    voice = get(bot.voice_clients, guild=ctx.guild)
    cur = str_loading_song
    cur.color = 0x487B60
    msg = await ctx.send(embed=cur)
    if voice.is_playing():
        voice.stop()
        current_song[ctx.guild.id] = {}
        song_queue[ctx.guild.id] = []
        await msg.edit(content = '', embed=str_not_song_playing)
    else:
        await msg.edit(content = '', embed=str_not_song_playing)

async def skipto(ctx, index, bot):
    voice = get(bot.voice_clients, guild=ctx.guild)
    cur = str_loading_song
    cur.color = 0x487B60
    msg = await ctx.send(embed=cur)
    if ctx.guild.id not in song_queue:
        await msg.edit(content = '', embed=str_no_song_next)
    elif voice.is_playing():
        if ctx.guild.id not in song_queue:
            await msg.edit(content = '', embed=str_no_song_next)
        elif len(song_queue[ctx.guild.id]) < index-1:
            await msg.edit(content = '', embed=str_exceds_songs)  
        else:
            for _ in range(index-2):
                song_queue[ctx.guild.id].pop(0)
            info = song_queue[ctx.guild.id][0]
            voice.stop()
            embedVar = discord.Embed(title=f'我来播放这首歌了捏', description=f'{info["title"]}\n{info["webpage_url"]}', color=0x8B4C39)
            await msg.edit(content='', embed=embedVar)
    else:
        await msg.edit(content='', embed=str_not_song_playing)

async def skip(ctx, bot):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        if ctx.guild.id not in song_queue:
            await ctx.send(embed=str_no_song_next)
        elif len(song_queue[ctx.guild.id]) != 0:
            info = song_queue[ctx.guild.id][0]
            embedVar = discord.Embed(title=f'我来播放这首歌了捏！', description=f'{info["title"]}\n{info["webpage_url"]}', color=0x8B4C39)
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(embed=str_no_song_next)
    else:
        await ctx.send(embed=str_not_song_playing)