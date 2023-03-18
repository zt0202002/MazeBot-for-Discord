import discord
from discord.utils import get
from help_functions.help_queue import current_song
from commands.cmd_queue import QUEUE_ID, update_queue
from commands.cmd_current import CURRENT_ID, current
from datetime import datetime

pause_time = {}

async def resume(ctx, bot, msg=None):
    global pause_time
    voice = get(bot.voice_clients, guild=ctx.guild)
    gid = ctx.guild.id

    if current_song[gid] is None or current_song[gid] == {}:
        embedVar = discord.Embed(title=f'没有歌曲在播放啦！', description=f'', color=0x487B60)

    if not voice.is_playing():
        voice.resume()
        current_song[gid]['time'] += datetime.now() - current_song[gid]['pauseTime']
        current_song[gid]['pauseTime'] = -1
        current_song[gid]['status'] = 'playing'
        embedVar = discord.Embed(title=f'歌曲又开始播放啦！', description=f'', color=0x487B60)
    else:
        embedVar = discord.Embed(title=f'歌曲已经在播放啦！', description=f'', color=0x487B60)

    if msg is not None and msg.id in QUEUE_ID:
        await update_queue(msg, 'resume')
    elif msg is not None and msg.id in CURRENT_ID:
        await current(ctx, bot, msg)
    elif msg is None:
        await ctx.send(embed=embedVar)
    else:
        await msg.edit(content = '', embed=embedVar)

async def pause(ctx, bot, msg=None):
    global pause_time
    voice = get(bot.voice_clients, guild=ctx.guild)
    gid = ctx.guild.id

    if current_song[gid] is None or current_song[gid] == {}:
        embedVar = discord.Embed(title=f'没有歌曲在播放啦！', description=f'', color=0x487B60)

    if voice.is_playing():
        voice.pause()
        pause_time[gid] = datetime.now()
        current_song[gid]['status'] = 'pause'
        current_song[gid]['pauseTime'] = datetime.now()
        embedVar = discord.Embed(title=f'歌曲被暂停啦！', description=f'', color=0x487B60)
    else:
        embedVar = discord.Embed(title=f'歌曲已经被暂停啦！', description=f'', color=0x487B60)

    if msg is not None and msg.id in QUEUE_ID:
        await update_queue(msg, 'pause')
    elif msg is not None and msg.id in CURRENT_ID:
        await current(ctx, bot, msg)
    elif msg is None:
        await ctx.send(embed=embedVar)
    else:
        await msg.edit(content = '', embed=embedVar)