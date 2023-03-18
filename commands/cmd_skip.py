from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from help_functions.help_queue import *
from commands.cmd_queue import update_queue, QUEUE_ID
from commands.cmd_current import current, CURRENT_ID
import asyncio

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
            embedVar = discord.Embed(title=f'我来播放这首歌了捏', description=f'{info.title}\n{info.watch_url}', color=0x8B4C39)
            await msg.edit(content='', embed=embedVar)
    else:
        await msg.edit(content='', embed=str_not_song_playing)

async def skip(ctx, bot, msg=None):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing() or current_song[ctx.guild.id] is not None or current_song[ctx.guild.id] != {}:
        voice.stop()
        if ctx.guild.id not in song_queue:
            embedVar = str_no_song_next
        elif len(song_queue[ctx.guild.id]) != 0:
            info = song_queue[ctx.guild.id][0]
            embedVar = discord.Embed(title=f'我来播放这首歌了捏！', description=f'{info.title}\n{info.watch_url}', color=0x8B4C39)
            
        else:
            embedVar = str_no_song_next
    else:
        embedVar = str_not_song_playing
    
    if msg is not None and msg.id in QUEUE_ID:
        await asyncio.sleep(1)
        await update_queue(msg, 'skip')
    elif msg is not None and msg.id in CURRENT_ID:
        await current(ctx, bot, msg)
    elif msg is None:
        await ctx.send(embed=embedVar)
    else:
        await msg.edit(content = '', embed=embedVar)