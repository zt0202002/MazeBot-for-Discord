from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from help_functions.help_queue import *
from discordhelp import getEmoteFromName
from commands.cmd_resume import *
from commands.cmd_skip import *

QUEUE_INDEX = {}
QUEUE_ID = []
NEXT_PAGE = 5

class QueueButton(discord.ui.View):
    global QUEUE_INDEX, QUEUE_ID, NEXT_PAGE

    def get_msg(self, interaction):
        self.timeout = None
        gid = interaction.guild.id
        index = QUEUE_INDEX[gid]
        return gid, index

    @discord.ui.button(label="Play | Paus", row=0, style=discord.ButtonStyle.primary)
    async def resume_button_callback(self, interaction, button):
        gid, index = self.get_msg(interaction)
        button = await resume(interaction, interaction.client, interaction.message)
        if button is False: await pause(interaction, interaction.client, interaction.message)

        # await asyncio.sleep(0.5)
        queue_list = await load_queue(interaction)
        await interaction.response.edit_message(content = '', embed=await convert_queue_to_embed(interaction, queue_list, QUEUE_INDEX[gid]), view=self)

    @discord.ui.button(label="Skip", row=0, style=discord.ButtonStyle.primary)
    async def skip_button_callback(self, interaction, button):
        gid, index = self.get_msg(interaction)
        await skip(interaction, interaction.client, interaction.message)

        # await asyncio.sleep(0.5)
        queue_list = await load_queue(interaction)
        await interaction.response.edit_message(content = '', embed=await convert_queue_to_embed(interaction, queue_list, QUEUE_INDEX[gid]), view=self)

    @discord.ui.button(label="Prev", row=0, style=discord.ButtonStyle.primary)
    async def prev_button_callback(self, interaction, button):
        gid, index = self.get_msg(interaction)
        queue_list = await load_queue(interaction)

        if index - NEXT_PAGE < 0:   index = 0
        else:   index -= NEXT_PAGE

        QUEUE_INDEX[gid] = index

        await interaction.response.edit_message(content = '', embed=await convert_queue_to_embed(interaction, queue_list, QUEUE_INDEX[gid]), view=self)

    @discord.ui.button(label="Next", row=0, style=discord.ButtonStyle.primary)
    async def next_button_callback(self, interaction, button):
        gid, index = self.get_msg(interaction)
        queue_list = await load_queue(interaction)

        if index + NEXT_PAGE >= len(queue_list):     index = len(queue_list) - NEXT_PAGE
        else:                                       index += NEXT_PAGE

        QUEUE_INDEX[gid] = index

        await interaction.response.edit_message(content = '', embed=await convert_queue_to_embed(interaction, queue_list, QUEUE_INDEX[gid]), view=self)

    @discord.ui.button(label="Load", row=0, style=discord.ButtonStyle.success)
    async def refresh_button_callback(self, interaction, button):
        gid, index = self.get_msg(interaction)
        queue_list = await load_queue(interaction)
        await interaction.response.edit_message(content = '', embed=await convert_queue_to_embed(interaction, queue_list, QUEUE_INDEX[gid]), view=self)

async def queue(ctx, bot, msg=None):
    global QUEUE_INDEX
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    cur = str_loading_song
    cur.color = 0x487B60
    if msg is None: msg = await ctx.send(embed=cur)

    queue_list = await load_queue(msg)

    QUEUE_INDEX[ctx.guild.id] = 0
    if ctx.guild.id not in QUEUE_ID:  QUEUE_ID.append(ctx.guild.id)

    await msg.edit(content = '', embed=await convert_queue_to_embed(ctx, queue_list, 0), view=QueueButton())

    

    # await add_emoji_options(msg)

    """
    # emoji = getEmoteFromName(":ok:")
    # no = getEmoteFromName(":no_entry_sign:")
    # await msg.add_reaction(emoji)
    # await msg.add_reaction(no)

    # # if ctx.guild.id not in current_song or current_song[ctx.guild.id] == {}:
    # if ctx.guild.id not in current_song or current_song[ctx.guild.id] == {}:
    #     msg = await msg.edit(content = '', embed=str_not_song_playing)
    # else:
    #     current = current_song[ctx.guild.id]['info']

    #     timer = check_time(current_song[ctx.guild.id])

    #     if ctx.guild.id not in song_queue or len(song_queue[ctx.guild.id]) == 0:
    #         embedVar = discord.Embed(title=f'当前播放:\n[1] {current["title"]} [{timer[0]}/{timer[1]}]\n', description=f'', color=0x487B60)
    #         msg = await msg.edit(content = '', embed=embedVar)
    #     else:
    #         queue = song_queue[ctx.guild.id]
    #         queue_list = ''
    #         for i in range(len(queue)):
    #             queue_list += f'[{i+2}]\t {queue[i].title}\n'
    #         embedVar = discord.Embed(title=f'当前播放:\n[1] {current["title"]} [{timer[0]}/{timer[1]}]\n', description=f'{queue_list}', color=0x487B60)
    #         msg = await msg.edit(content = '', embed=embedVar)

    # emoji = getEmoteFromName(":ok:")
    # no = getEmoteFromName(":no_entry_sign:")
    # await msg.add_reaction(emoji)
    # await msg.add_reaction(no)
    """

async def add_emoji_options(msg):
    await msg.clear_reactions()

    next_page = getEmoteFromName(":arrow_right:")
    prev_page = getEmoteFromName(":arrow_left:")
    refresh = getEmoteFromName(":arrows_counterclockwise:")
    
    pause = getEmoteFromName(":pause_button:")
    play = getEmoteFromName(":arrow_forward:")
    skip = getEmoteFromName(":track_next:")

    await msg.add_reaction(pause)
    await msg.add_reaction(play)
    await msg.add_reaction(skip)
    await msg.add_reaction(prev_page)
    await msg.add_reaction(next_page)
    await msg.add_reaction(refresh)

async def update_queue(msg, option):
    global QUEUE_INDEX
    queue_list = await load_queue(msg)
    if option == 'next':
        QUEUE_INDEX[msg.id] += NEXT_PAGE
        if QUEUE_INDEX[msg.id] > len(queue_list): QUEUE_INDEX[msg.id] -= NEXT_PAGE
    elif option == 'prev':
        QUEUE_INDEX[msg.id] -= NEXT_PAGE
        if QUEUE_INDEX[msg.id] < 0: QUEUE_INDEX[msg.id] = 0        
    await msg.edit(content = '', embed=await convert_queue_to_embed(msg, queue_list, QUEUE_INDEX[msg.id]))

    await add_emoji_options(msg)

async def convert_queue_to_embed(ctx, queue_list, start, end=NEXT_PAGE):
    if queue_list is None or len(queue_list) == 0:    return str_not_song_playing
    if start > len(queue_list): return str_not_song_playing
    if start < 0: start = 0
    
    if start+end > len(queue_list):   end = len(queue_list)
    else:   end = start+end

    if start == 0:  
        start = 1
        current = queue_list[0]['info']
    else:
        current = None
    
    timer = check_time(current_song[ctx.guild.id])
    queue = queue_list[start:end]

    status = '正在播放' if queue_list[0]['status'] == 'playing' else '已暂停'

    embedVar = discord.Embed(title=f'Current Playlist', description="", color=0x8B4C39)

    if len(queue) == 0 and current is not None:
        embedVar.add_field(name=f'**[1] {current["title"]} [{timer[0]}|{timer[1]}] [{status}]**', value=f'', inline=False)
    else:
        queue_list = ''
        if current is not None:
            embedVar.add_field(name=f'**[1] {current["title"]} [{timer[0]}|{timer[1]}] [{status}]**', value=f'', inline=False)
        for i in range(len(queue)):
            try:
                try:    embedVar.add_field(name=f'**[{start+i+1}] {queue[i].title}**', value=f'', inline=False)
                except: embedVar.add_field(name=f'**[{start+i+1}] {queue[i]["title"]}**', value=f'', inline=False)
            except:
                embedVar.add_field(name=f'**f[{start+i+1}]\t Error Title | Will be deleted automatically\n**', value=f'', inline=False)
                # delete song from queue
                song_queue[ctx.guild.id].pop(i)
    return embedVar

async def load_queue(msg):
    queue_list = []
    # if ctx.guild.id not in current_song or current_song[ctx.guild.id] == {}:
    if msg.guild.id not in current_song or current_song[msg.guild.id] == {}:
        # msg = await msg.edit(content = '', embed=str_not_song_playing)
        return None
    else:
        current = current_song[msg.guild.id]['info']
        timer = check_time(current_song[msg.guild.id])

        queue_list.append(current_song[msg.guild.id])
        for i in range(len(song_queue[msg.guild.id])):
            queue_list.append(song_queue[msg.guild.id][i])

        return queue_list



        if ctx.guild.id not in song_queue or len(song_queue[ctx.guild.id]) == 0:
            queue_list.append(current)
            embedVar = discord.Embed(title=f'当前播放:\n[1] {current["title"]} [{timer[0]}/{timer[1]}]\n', description=f'', color=0x487B60)
            msg = await msg.edit(content = '', embed=embedVar)
        else:
            queue = song_queue[ctx.guild.id]
            queue_list = ''
            for i in range(len(queue)):
                queue_list += f'[{i+2}]\t {queue[i].title}\n'
            embedVar = discord.Embed(title=f'当前播放:\n[1] {current["title"]} [{timer[0]}/{timer[1]}]\n', description=f'{queue_list}', color=0x487B60)
            msg = await msg.edit(content = '', embed=embedVar)

