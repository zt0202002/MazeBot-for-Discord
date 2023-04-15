from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from discord import FFmpegPCMAudio
# from youtube_dl import YoutubeDL
from yt_dlp import YoutubeDL
from help_functions.help_queue import *
from commands.cmd_join import join
from discord import Message
from commands import cmd_search
import asyncio

import validators
from pytube import Playlist, YouTube as yt

async def play_music(ctx, bot, msg, new_song_len):
    # voice = get(bot.voice_clients, guild=ctx.guild)
    if isinstance(ctx, Message):
        voice = ctx.guild.voice_client
    else:
        voice = ctx.message.guild.voice_client
    
    cur_len = len(song_queue[ctx.guild.id])
    is_edit_msg = False

    # 没有歌曲播放的话，就播放queue中的第一首歌
    if not voice.is_playing():
        await asyncio.sleep(1.5)
        cur_info = song_queue[ctx.guild.id].pop(0)
        url = None
        while len(song_queue[ctx.guild.id]) > 0:
            try:
                try:    url = cur_info.watch_url
                except: 
                    if 'webpage_url' in cur_info:   url = cur_info['webpage_url']
                    else:                           url = cur_info['url']
                break
            except:
                cur_info = song_queue[ctx.guild.id].pop(0)
        if url is None:
            print('ERROR: WRONG MUSIC URL')
            return

        with YoutubeDL(YDL_OPTIONS) as ydl: cur_info = ydl.extract_info(url, download=False)

        temp = {}; temp['info'] = cur_info; temp['time'] = datetime.now(); temp['status'] = 'playing'
        temp['pauseTime'] = -1
        current_song[ctx.guild.id] = temp
        timer = check_time(temp)
        source = FFmpegPCMAudio(cur_info['url'], **FFMPEG_OPTIONS)
        voice.play(source, after=lambda x=0: check_queue(ctx, ctx.guild.id))
        embedVar = discord.Embed(title=f'我来播放这首歌了捏！', description=f'{cur_info["title"]}\n[{timer[0]}/{timer[1]}]\n{url}', color=0x8B4C39)
        
        if msg is None: await ctx.channel.send(embed=embedVar)
        else:           await msg.edit(content='', embed=embedVar)
        is_edit_msg = True
    
    # 如果当前有歌曲播放，且如果只有一首新歌，print出来这首歌的名字和url
    elif new_song_len == 1:
        new_song = song_queue[ctx.guild.id][cur_len - 1]

        try:    url = new_song.watch_url
        except: 
            if 'webpage_url' in new_song:   url = new_song['webpage_url']
            else:                   url = new_song['url']
        
        try:    embedVar = discord.Embed(title=f'我把这首歌加入播放列表了捏！', description=f'[{cur_len+1}]\t{new_song.title}\n{url}', color=0x8B4C39)
        except: embedVar = discord.Embed(title=f'我把这首歌加入播放列表了捏！', description=f'[{cur_len+1}]\t{new_song["title"]}\n{url}', color=0x8B4C39)
        if msg is None: await ctx.channel.send(embed=embedVar)
        else:           await msg.edit(content='', embed=embedVar)
        is_edit_msg = True
    
    # 如果新加入的歌不只一首，print出来专辑中的歌的数量
    if new_song_len > 1:
        # embedVar = discord.Embed(title=f'专辑{info["title"]}中的{len(info["entries"])}首歌加入到播放列表了捏！', description="", color=0x8B4C39)
        embedVar = discord.Embed(title=f'已经将{new_song_len}首歌加入到播放列表了捏！', description="", color=0x8B4C39)
        if is_edit_msg or msg is None: await ctx.channel.send(embed=embedVar)
        else:           await msg.edit(content='', embed=embedVar)

    try:    await asyncio.wait_for(check_queue_correct(ctx.guild.id), timeout=5)
    except: pass
    
async def check_queue_correct(gid):
    for i in range(len(song_queue[gid])):
        try:
            try:    url = song_queue[gid][i].watch_url
            except: url = song_queue[gid][i]['url']

            try:    title = song_queue[gid][i].title
            except: title = song_queue[gid][i]['title']
        except:
            try:    
                video = await asyncio.wait_for(asyncio.to_thread(yt, url), timeout=1)
                song_queue[gid][i].title = video.title
            except: song_queue[gid].pop(i)