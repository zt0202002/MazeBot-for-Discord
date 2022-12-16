from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from help_functions.help_queue import *

async def search(ctx, request, bot):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice is None:
        await ctx.send(embed=str_not_in_voice_channel)
        return
    elif voice.channel != ctx.message.author.voice.channel:
        await ctx.send(embed=str_not_in_same_channel)
        return
    
    msg = await ctx.send(embed=str_loading_song)
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{request}", download=False)['entries'][0]
        except:
            info = ydl.extract_info(request, download=False)
        
        if not info:
            embedVar = discord.Embed(title=f'我找不到这首歌啊喂！', description="", color=0x8B4C39)
            await msg.edit(content = '', embed=embedVar)
            return

        url = info['url']
        source = FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        if not voice.is_playing():
            voice.play(source, after=lambda x=0: check_queue(ctx, ctx.guild.id))
            temp = {}; temp['info'] = info; temp['time'] = datetime.now()
            current_song[ctx.guild.id] = temp
            timer = check_time(temp)
            embedVar = discord.Embed(title=f'我来播放这首歌了捏！', description=f'{info["title"]}\n[{timer[0]}/{timer[1]}]\n{info["webpage_url"]}', color=0x8B4C39)
            await msg.edit(content = '',  embed=embedVar)
        else:
            await addToQueue(ctx.guild, info)
            embedVar = discord.Embed(title=f'我把这首歌加入播放列表了捏！', description=f'[{len(song_queue[ctx.guild.id])}] - {info["title"]}', color=0x8B4C39)
            await msg.edit(content = '', embed=embedVar)
