from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from help_functions.help_queue import *

async def play(ctx, url, bot):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice is None:   await ctx.send(embed=str_not_in_voice_channel)
    elif voice.channel != ctx.message.author.voice.channel: await ctx.send(embed=str_not_in_same_channel)
    elif 'music.163.com' in url:    await ctx.send(embed=str_no_netease)
    else:
        msg = await ctx.send(embed=str_loading_song)        
        with YoutubeDL(YDL_OPTIONS) as ydl: info = ydl.extract_info(url, download=False)
        
        if "entries" not in info:
            url = info['url']
            source = FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
            if not voice.is_playing():
                voice.play(source, after=lambda x=0: check_queue(ctx, ctx.guild.id))
                temp = {}; temp['info'] = info; temp['time'] = datetime.now()
                current_song[ctx.guild.id] = temp
                timer = check_time(temp)
                embedVar = discord.Embed(title=f'我来播放这首歌了捏！', description=f'{info["title"]}\n[{timer[0]}/{timer[1]}]\n{info["webpage_url"]}', color=0x8B4C39)
                await msg.edit(content='', embed=embedVar)
            else:
                await addToQueue(ctx.guild, info)
                temp_len = len(song_queue[ctx.guild.id])
                if temp_len == 0: temp_len = 1
                else: temp_len += 2
                embedVar = discord.Embed(title=f'我把这首歌加入播放列表了捏！', description=f'[{temp_len}]\t{info["title"]}\n{info["webpage_url"]}', color=0x8B4C39)
                await msg.edit(content='', embed=embedVar)
        else:
            await addToQueue(ctx.guild, info, ctx)
            if not voice.is_playing():
                cur_info = song_queue[ctx.guild.id].pop(0)
                temp = {}; temp['info'] = cur_info; temp['time'] = datetime.now()
                current_song[ctx.guild.id] = temp
                timer = check_time(temp)
                source = FFmpegPCMAudio(cur_info['url'], **FFMPEG_OPTIONS)
                voice.play(source, after=lambda x=0: check_queue(ctx, ctx.guild.id))
                embedVar = discord.Embed(title=f'我来播放这首歌了捏！', description=f'{cur_info["title"]}\n[{timer[0]}/{timer[1]}]\n{cur_info["webpage_url"]}', color=0x8B4C39)
                await msg.edit(content='', embed=embedVar)
            embedVar = discord.Embed(title=f'专辑{info["title"]}中的{len(info["entries"])}首歌加入到播放列表了捏！', description="", color=0x8B4C39)
            await msg.edit(content = '', embed=embedVar)