from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL
from help_functions.help_queue import *
from commands.cmd_play import play_music
from commands.cmd_queue import NEXT_PAGE
from commands.cmd_join import join

from discordhelp import getEmoteFromName


SEARCH_INDEX = {}
SEARCH_QUEUE = {}
SEARCH_ID = []

async def search(ctx, request, bot, msg=None):
    global SEARCH_INDEX, SEARCH_QUEUE, SEARCH_MSG_ID
    voice = get(bot.voice_clients, guild=ctx.guild)
    if msg is not None: channel = ctx.author.voice.channel
    else:   channel = ctx.message.author.voice.channel

    embedVar = None
    if voice is None:               
        # embedVar = str_not_in_voice_channel
        msg = await join(ctx, bot, msg)
    elif voice.channel != channel:      
        embedVar = str_not_in_same_channel
        if msg is None: await ctx.send(embed=embedVar)
        else:           await msg.edit(content='', embed=embedVar) 

    
    if msg is None: msg = await ctx.send(embed=str_loading_song)

    SEARCH_ID.append(msg.id)
    
    with YoutubeDL(YDL_OPTIONS) as ydl:
        global SEARCH_QUEUE, SEARCH_INDEX
        try:    infos = ydl.extract_info(f"ytsearch10:{request}", download=False)['entries']
        except: info = ydl.extract_info(request, download=False)

        if not infos:
            embedVar = discord.Embed(title=f'我找不到这首歌啊喂！', description="", color=0x8B4C39)
            await msg.edit(content = '', embed=embedVar)
            return

        print(len(infos))
        # print(len(info))

        SEARCH_QUEUE[ctx.guild.id] = infos
        SEARCH_INDEX[ctx.guild.id] = 0

        queue_list_embed = await conver_search_queue_to_embed(infos, 0)        
        msg = await msg.edit(content = '', embed=queue_list_embed)
        await add_emoji_options(msg)
        

        # print(info['webpage_url'])

        # url = info['url']
        # source = FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        # if not voice.is_playing():
        #     voice.play(source, after=lambda x=0: check_queue(ctx, ctx.guild.id))
        #     temp = {}; temp['info'] = info; temp['time'] = datetime.now()
        #     current_song[ctx.guild.id] = temp
        #     timer = check_time(temp)
        #     embedVar = discord.Embed(title=f'我来播放这首歌了捏！', description=f'{info["title"]}\n[{timer[0]}/{timer[1]}]\n{info["webpage_url"]}', color=0x8B4C39)
        #     await msg.edit(content = '',  embed=embedVar)
        # else:
        #     await addToQueue(ctx.guild, info)
        #     embedVar = discord.Embed(title=f'我把这首歌加入播放列表了捏！', description=f'[{len(song_queue[ctx.guild.id])}] - {info["title"]}', color=0x8B4C39)
        #     await msg.edit(content = '', embed=embedVar)

async def add_emoji_options(msg):
    await msg.clear_reactions()

    one = getEmoteFromName(':one:')
    two = getEmoteFromName(':two:')
    three = getEmoteFromName(':three:')
    four = getEmoteFromName(':four:')
    five = getEmoteFromName(':five:')

    next_page = getEmoteFromName(':arrow_right:')
    prev_page = getEmoteFromName(':arrow_left:')

    await msg.add_reaction(prev_page)
    await msg.add_reaction(one)
    await msg.add_reaction(two)
    await msg.add_reaction(three)
    await msg.add_reaction(four)
    await msg.add_reaction(five)
    await msg.add_reaction(next_page)

async def update_queue(ctx, bot, msg, option):
    global SEARCH_INDEX, SEARCH_QUEUE
    infos = SEARCH_QUEUE[msg.guild.id]
    index = SEARCH_INDEX[msg.guild.id]

    if option == 1:
        await addToQueue(ctx.guild, url = infos[index]['webpage_url'])
        await play_music(ctx, bot, None, 1)
    elif option == 2:
        await addToQueue(ctx.guild, url = infos[index+1]['webpage_url'])
        await play_music(ctx, bot, None, 1)
    elif option == 3:
        await addToQueue(ctx.guild, url = infos[index+2]['webpage_url'])
        await play_music(ctx, bot, None, 1)
    elif option == 4:
        await addToQueue(ctx.guild, url = infos[index+3]['webpage_url'])
        await play_music(ctx, bot, None, 1)
    elif option == 5:
        await addToQueue(ctx.guild, url = infos[index+4]['webpage_url'])
        await play_music(ctx, bot, None, 1)
    elif option == 'next':
        if index + NEXT_PAGE >= len(infos): return
        index += NEXT_PAGE
        SEARCH_INDEX[msg.guild.id] = index
    elif option == 'prev':
        if index - NEXT_PAGE < 0: return
        index -= NEXT_PAGE
        SEARCH_INDEX[msg.guild.id] = index

    queue_list_embed = await conver_search_queue_to_embed(infos, index)
    await msg.edit(content = '', embed=queue_list_embed)
    await add_emoji_options(msg)

async def conver_search_queue_to_embed(infos, start, end=NEXT_PAGE):
    embedVar = discord.Embed(title=f'我找到了这些歌！', description="", color=0x8B4C39)
    if start + end > len(infos): end = len(infos)
    else: end += start
    for i in range(start, end):
        embedVar.add_field(name=f'**[{i+1}] {infos[i]["title"]}**', value=f'{infos[i]["webpage_url"]}', inline=False)
    return embedVar