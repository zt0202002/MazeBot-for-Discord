from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from help_functions.help_queue import *
from os.path import exists

from commands import cmd_play

async def loading_queue(ctx, type, bot):
    voice = get(bot.voice_clients, guild=ctx.guild)
 
    if voice is None:   await ctx.send(embed=str_not_in_voice_channel)
    elif voice.channel != ctx.message.author.voice.channel: await ctx.send(embed=str_not_in_same_channel)
    else:
        msg = await ctx.send(embed=str_loading_song)
        if type == 'Server History':
            song_len = await load_queue_from_file(ctx.guild)
            embedVar = discord.Embed(title=f'上次播放列表中没有未播完的歌，我就不加入到播放列表了捏！', description="", color=0x8B4C39)
        elif type == 'Mine':
            song_len = await load_queue_from_file(ctx.guild, "UserPlaylist", ctx.author.id)
            embedVar = discord.Embed(title=f'当前我这儿没有你存放的播放列表，我就不加入到播放列表了捏！', description="", color=0x8B4C39)
        if song_len == 0:
            await msg.edit(content = '', embed=embedVar)
            return

        await cmd_play.play_music(ctx, bot, msg, song_len)
        
        # embedVar = discord.Embed(title=f'已经将{song_len}首歌加入到播放列表了捏！', description="", color=0x8B4C39)
        # if not voice.is_playing():
        #     cur_info = song_queue[ctx.guild.id].pop(0)
        #     temp = {}; temp['info'] = cur_info; temp['time'] = datetime.now()
        #     current_song[ctx.guild.id] = temp
        #     timer = check_time(temp)
        #     source = FFmpegPCMAudio(cur_info['url'], **FFMPEG_OPTIONS)
        #     voice.play(source, after=lambda x=0: check_queue(ctx, ctx.guild.id))
        #     playing_embedVar = discord.Embed(title=f'我来播放这首歌了捏！', description=f'{cur_info["title"]}\n[{timer[0]}/{timer[1]}]\n{cur_info["webpage_url"]}', color=0x8B4C39)
        #     await msg.edit(content='', embed=playing_embedVar)
        #     await ctx.channel.send(content = '', embed=embedVar)
        # else:
        #     # embedVar = discord.Embed(title=f'上次播放列表中有{song_len}首未播完的歌，我把它们加入到播放列表了捏！', description="", color=0x8B4C39)
        #     await msg.edit(content = '', embed=embedVar)

async def save_url_to_file(ctx, url, bot):
    msg = await ctx.send(embed=str_loading_song)

    # with YoutubeDL(YDL_OPTIONS) as ydl: info = ydl.extract_info(url, download=False)
    # if "playlist?list=" not in url: msg.edit(embed=str_not_playlist); return

    try:        playlist = Playlist(url)
    except:     msg.edit(embed=str_not_playlist); return

    with open(f'./QueueLog/UserPlaylist/{ctx.author.id}.json', 'w') as f:   f.write(url)

    str_save_playlist = discord.Embed(title=f'专辑{playlist.title}保存到播放列表了捏！', description="", color=0x8B4C39)
    await msg.edit(embed=str_save_playlist)
