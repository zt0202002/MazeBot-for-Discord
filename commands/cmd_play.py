from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from discord import FFmpegPCMAudio
# from youtube_dl import YoutubeDL
from yt_dlp import YoutubeDL
from help_functions.help_queue import *
from commands.cmd_join import join
from discord import Message
from commands import cmd_search, cmd_play_music

import validators

async def play(ctx, url, bot, msg = None):
    voice = get(bot.voice_clients, guild=ctx.guild)
    try:    channel = ctx.author.voice.channel
    except: channel = ctx.message.channel

    if voice is None:
        msg = await join(ctx, bot, msg)
        # if msg is None:     await ctx.send(embed=str_not_in_voice_channel); return
        # else:               await msg.edit(content='', embed=str_not_in_voice_channel); return
    elif voice.channel != channel:
        if msg is None:     await ctx.send(embed=str_not_in_same_channel);  return
        else:               await msg.edit(content='', embed=str_not_in_same_channel);  return
    elif 'music.163.com' in url:    
        if msg is None:     await ctx.send(embed=str_no_netease);   return
        else:               await msg.edit(content='', embed=str_no_netease);   return

    if not validators.url(url): await cmd_search.search(ctx, url, bot, msg); return

    if msg is None: msg = await ctx.send(embed=str_loading_song)   

    new_song_len = await addToQueue(ctx.guild, url = url)



    if not new_song_len:    await msg.edit(content='', embed=str_invalid_url)
    else:                   await cmd_play_music.play_music(ctx, bot, msg, new_song_len)