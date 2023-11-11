import discord
from discord.utils import get
from help_functions.help_text import *
from commands.music.music_playlist import player
from datetime import datetime
import asyncio



async def resume(ctx, bot, msg=None):
    voice = get(bot.voice_clients, guild=ctx.guild)
    gid = ctx.guild.id
    curr_info = player.get_curr(gid)

    if curr_info == {}:
        embedVar = discord.Embed(title=f'没有歌曲在播放啦！', description=f'', color=FAILURE)
        if msg is None: await ctx.send(embed=embedVar)

    if not voice.is_playing():
        voice.resume()
        player.set_curr(gid, curr_info, '[正在播放]', start=curr_info['start']+(datetime.now()-curr_info['pause']), pause=None)
        
        embedVar = discord.Embed(title=f'歌曲又开始播放啦！', description=f'', color=SUCCESS)
        if msg is None: await ctx.send(embed=embedVar)
        await asyncio.sleep(0.5)
    else:
        embedVar = discord.Embed(title=f'歌曲已经在播放啦！', description=f'', color=FAILURE)
        if msg is None: await ctx.send(embed=embedVar)
        else: await msg.edit(content='', embed=embedVar)

async def pause(ctx, bot, msg=None):
    voice = get(bot.voice_clients, guild=ctx.guild)
    gid = ctx.guild.id
    curr_info = player.get_curr(gid)

    if curr_info == {}:
        embedVar = discord.Embed(title=f'没有歌曲在播放啦！', description=f'', color=FAILURE)
        if msg is None: await ctx.send(embed=embedVar)
    
    if voice.is_playing():
        voice.pause()
        player.set_curr(gid, curr_info, '[已暂停]', start=curr_info['start'], pause=datetime.now())
        embedVar = discord.Embed(title=f'歌曲被暂停啦！', description=f'', color=SUCCESS)
        if msg is None: await ctx.send(embed=embedVar)
        await asyncio.sleep(0.5)
    else:
        embedVar = discord.Embed(title=f'歌曲已经被暂停啦！', description=f'', color=FAILURE)
        if msg is None: await ctx.send(embed=embedVar)
        else:           await msg.edit(content='', embed=embedVar)