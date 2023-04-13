from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL
from pytube import Search
from help_functions.help_queue import *
from commands.cmd_play_music import play_music
from commands.cmd_queue import NEXT_PAGE
from commands.cmd_join import join

from discordhelp import getEmoteFromName


SEARCH_INDEX = {}
SEARCH_QUEUE = {}
SEARCH_ID = []

class SeachButton(discord.ui.View):
    global SEARCH_INDEX, SEARCH_QUEUE
    
    def get_msg(self, interaction):
        msg_id = interaction.message.id
        infos = SEARCH_QUEUE[msg_id]
        index = SEARCH_INDEX[msg_id]
        return  msg_id, infos, index
    
    @discord.ui.button(label="1", row=0, style=discord.ButtonStyle.primary, timeout=None)
    async def first_button_callback(self, interaction, button):
        msg_id, infos, index = self.get_msg(interaction)
        
        watch_url = infos[index].watch_url
        await addToQueue(interaction.guild, url = watch_url)
        await play_music(interaction, interaction.client, None, 1)

        queue_list_embed = await conver_search_queue_to_embed(infos, index)
        await interaction.response.edit_message(content = '', embed=queue_list_embed, view=self)
    
    @discord.ui.button(label="2", row=0, style=discord.ButtonStyle.primary, timeout=None)
    async def second_button_callback(self, interaction, button):
        msg_id, infos, index = self.get_msg(interaction)
        
        watch_url = infos[index+1].watch_url
        await addToQueue(interaction.guild, url = watch_url)
        await play_music(interaction, interaction.client, None, 1)

        queue_list_embed = await conver_search_queue_to_embed(infos, index)
        await interaction.response.edit_message(content = '', embed=queue_list_embed, view=self)

    @discord.ui.button(label="3", row=0, style=discord.ButtonStyle.primary, timeout=None)
    async def third_button_callback(self, interaction, button):
        msg_id, infos, index = self.get_msg(interaction)
        
        watch_url = infos[index+2].watch_url
        await addToQueue(interaction.guild, url = watch_url)
        await play_music(interaction, interaction.client, None, 1)

        queue_list_embed = await conver_search_queue_to_embed(infos, index)
        await interaction.response.edit_message(content = '', embed=queue_list_embed, view=self)

    @discord.ui.button(label="4", row=0, style=discord.ButtonStyle.primary, timeout=None)
    async def forth_button_callback(self, interaction, button):
        msg_id, infos, index = self.get_msg(interaction)
        
        watch_url = infos[index+3].watch_url
        await addToQueue(interaction.guild, url = watch_url)
        await play_music(interaction, interaction.client, None, 1)

        queue_list_embed = await conver_search_queue_to_embed(infos, index)
        await interaction.response.edit_message(content = '', embed=queue_list_embed, view=self)

    @discord.ui.button(label="5", row=0, style=discord.ButtonStyle.primary, timeout=None)
    async def fifth_button_callback(self, interaction, button):
        msg_id, infos, index = self.get_msg(interaction)
        
        try:
            watch_url = infos[index+4].watch_url
        except:
            embedVar = discord.Embed(title="Error", description="Loading video failed, please try again", color=0x00ff00)
            interaction.response.send_message(content = '', embed=embedVar)
            await interaction.response.edit_message(content = '', embed=queue_list_embed, view=self)
            return
        await addToQueue(interaction.guild, url = watch_url)
        await play_music(interaction, interaction.client, None, 1)

        queue_list_embed = await conver_search_queue_to_embed(infos, index)
        await interaction.response.edit_message(content = '', embed=queue_list_embed, view=self)


    @discord.ui.button(label="Prev", row=1, style=discord.ButtonStyle.success, timeout=None)
    async def next_button_callback(self, interaction, button):
        msg_id, infos, index = self.get_msg(interaction)

        if index - NEXT_PAGE < 0:
            queue_list_embed = await conver_search_queue_to_embed(infos, index)
            await interaction.response.edit_message(content = '', embed=queue_list_embed, view=self)
        else:
            index -= NEXT_PAGE
            SEARCH_INDEX[msg_id] = index

            queue_list_embed = await conver_search_queue_to_embed(infos, index)
            await interaction.response.edit_message(content = '', embed=queue_list_embed, view=self)

        # await interaction.message.edit(content="You pressed me!") 

    @discord.ui.button(label="Next", row=1, style=discord.ButtonStyle.success, timeout=None)
    async def prev_button_callback(self, interaction, button):
        msg_id, infos, index = self.get_msg(interaction)

        if index + NEXT_PAGE >= len(infos) - 5:
            queue_list_embed = await conver_search_queue_to_embed(infos, index)
            await interaction.response.edit_message(content = '', embed=queue_list_embed, view=self)
        else:
            index += NEXT_PAGE
            SEARCH_INDEX[msg_id] = index

            queue_list_embed = await conver_search_queue_to_embed(infos, index)
            await interaction.response.edit_message(content = '', embed=queue_list_embed, view=self)
    
    

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
    
    search_results = Search(request).results

    SEARCH_QUEUE[msg.id] = search_results
    SEARCH_INDEX[msg.id] = 0

    queue_list_embed = await conver_search_queue_to_embed(search_results, 0)        
    msg = await msg.edit(content = '', embed=queue_list_embed, view=SeachButton())
    # await add_emoji_options(msg)

    """
    # with YoutubeDL(YDL_OPTIONS) as ydl:
    #     global SEARCH_QUEUE, SEARCH_INDEX
    #     try:    infos = ydl.extract_info(f"ytsearch10:{request}", download=False)['entries']
    #     except: info = ydl.extract_info(request, download=False)

    #     if not infos:
    #         embedVar = discord.Embed(title=f'我找不到这首歌啊喂！', description="", color=0x8B4C39)
    #         await msg.edit(content = '', embed=embedVar)
    #         return

    #     print(len(infos))
    #     # print(len(info))

    #     SEARCH_QUEUE[ctx.guild.id] = infos
    #     SEARCH_INDEX[ctx.guild.id] = 0

    #     queue_list_embed = await conver_search_queue_to_embed(infos, 0)        
    #     msg = await msg.edit(content = '', embed=queue_list_embed)
    #     await add_emoji_options(msg)
        

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
        """
   

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

    try:
        if isinstance(option, int):
            watch_url = infos[index+option-1].watch_url
            await addToQueue(ctx.guild, url = watch_url)
            await play_music(ctx, bot, None, 1)
        elif option == 'next':
            if index + NEXT_PAGE >= len(infos): return
            index += NEXT_PAGE
            SEARCH_INDEX[msg.guild.id] = index
        elif option == 'prev':
            if index - NEXT_PAGE < 0: return
            index -= NEXT_PAGE
            SEARCH_INDEX[msg.guild.id] = index
    except:
        print('error')
        pass

    queue_list_embed = await conver_search_queue_to_embed(infos, index)
    await msg.edit(content = '', embed=queue_list_embed)
    await add_emoji_options(msg)

async def conver_search_queue_to_embed(infos, start, end=NEXT_PAGE):
    embedVar = discord.Embed(title=f'我找到了这些歌！', description="", color=0x8B4C39)
    if start + end > len(infos): end = len(infos)
    else: end += start
    for i in range(start, end):
        embedVar.add_field(name=f'**[{i+1}] {infos[i].title}**', value=f'{infos[i].watch_url}', inline=False)
    return embedVar