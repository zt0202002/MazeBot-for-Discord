from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from help_functions.help_queue import *
from discordhelp import getEmoteFromName
from commands.cmd_resume import *
from commands.cmd_skip import *
from pytube import Playlist, YouTube as yt

import urllib.request
import json
import urllib
import asyncio

QUEUE_INDEX = {}
QUEUE_ID = []
NEXT_PAGE = 5


class QueueButton(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    def get_msg(self, interaction):
        gid = interaction.guild.id
        index = QUEUE_INDEX[gid]
        self.mid = interaction.message.id
        return gid, index

    @discord.ui.button(label="<<", row=0, style=discord.ButtonStyle.primary, disabled=False)
    async def first_button_callback(self, interaction, button):
        button.view.timeout = None
        gid, index = self.get_msg(interaction)
        queue_list = await load_queue(interaction)

        index = 0

        QUEUE_INDEX[gid] = index

        await interaction.response.edit_message(content = '', embed=await convert_queue_to_embed(interaction, queue_list, QUEUE_INDEX[gid]), view=self)

    @discord.ui.button(label="<", row=0, style=discord.ButtonStyle.primary, disabled=False)
    async def prev_button_callback(self, interaction, button):
        button.view.timeout = None
        gid, index = self.get_msg(interaction)
        queue_list = await load_queue(interaction)

        if index - NEXT_PAGE < 0:   index = 0
        else:   index -= NEXT_PAGE

        QUEUE_INDEX[gid] = index

        await interaction.response.edit_message(content = '', embed=await convert_queue_to_embed(interaction, queue_list, QUEUE_INDEX[gid]), view=self)

    @discord.ui.button(label='⏯', row=0, style=discord.ButtonStyle.primary)
    async def resume_button_callback(self, interaction, button):
        button.view.timeout = None
        gid, index = self.get_msg(interaction)
        button = await resume(interaction, interaction.client, interaction.message)
        if button is False: 
            await pause(interaction, interaction.client, interaction.message)

        queue_list = await load_queue(interaction)
        await interaction.response.edit_message(content = '', embed=await convert_queue_to_embed(interaction, queue_list, QUEUE_INDEX[gid]), view=self)

    @discord.ui.button(label=">", row=0, style=discord.ButtonStyle.primary, disabled=False)
    async def next_button_callback(self, interaction, button):
        button.view.timeout = None
        gid, index = self.get_msg(interaction)
        queue_list = await load_queue(interaction)

        if index + NEXT_PAGE >= len(queue_list):    index = len(queue_list) - NEXT_PAGE
        else:                                       index += NEXT_PAGE

        QUEUE_INDEX[gid] = index

        await interaction.response.edit_message(content = '', embed=await convert_queue_to_embed(interaction, queue_list, QUEUE_INDEX[gid]), view=self)
    
    @discord.ui.button(label=">>", row=0, style=discord.ButtonStyle.primary, disabled=False)
    async def last_button_callback(self, interaction, button):
        button.view.timeout = None
        gid, index = self.get_msg(interaction)
        queue_list = await load_queue(interaction)

        index = len(queue_list) - NEXT_PAGE

        QUEUE_INDEX[gid] = index

        await interaction.response.edit_message(content = '', embed=await convert_queue_to_embed(interaction, queue_list, QUEUE_INDEX[gid]), view=self)
    
    @discord.ui.button(label="Skip", row=1, style=discord.ButtonStyle.success)
    async def skip_button_callback(self, interaction, button):
        button.view.timeout = None
        gid, index = self.get_msg(interaction)
        await skip(interaction, interaction.client, interaction.message)

        # await asyncio.sleep(0.5)
        queue_list = await load_queue(interaction)
        
        if queue_list != None:
            for i in range(0, len(queue_list)):
                if queue_list[i]['status'] == 'playing':
                    QUEUE_INDEX[gid] = i
                    break
        await interaction.response.edit_message(content = '', embed=await convert_queue_to_embed(interaction, queue_list, QUEUE_INDEX[gid]), view=self)

    @discord.ui.button(label="Fresh", row=1, style=discord.ButtonStyle.success)
    async def refresh_button_callback(self, interaction, button):
        button.view.timeout = None
        gid, index = self.get_msg(interaction)
        queue_list = await load_queue(interaction)            


        for i in range(1: len(queue_list)):
            try:
                try:    title = queue_list[i]['title']
                except: 
                    title = queue_list[i].title
                    if 'Error Title |' not in title:    continue
                    video = yt(queue_list[i].url)
                    title = video.title
                    queue_list[i].title = title
            except Exception as e:
                queue_list[i].title = 'Error Title | Title will show by Fresh button'

        await interaction.response.edit_message(content = '', embed=await convert_queue_to_embed(interaction, queue_list, QUEUE_INDEX[gid]), view=self)

    @discord.ui.button(label="x", row=1, style=discord.ButtonStyle.danger)
    async def delete_button_callback(self, interaction, button):
        def Is_bot(m):  return m.id == self.mid

        button.view.timeout = None
        gid, index = self.get_msg(interaction)
        QUEUE_ID.remove(gid)
        
        await interaction.channel.purge(limit=100, check=Is_bot)


async def queue(ctx, bot, msg=None):
    global QUEUE_INDEX, QUEUE_ID, NEXT_PAGE, PLAY_BUTTON, NEXT_BUTTON, PREV_BUTTON
    voice = get(bot.voice_clients, guild=ctx.guild)

    cur = str_loading_song
    cur.color = 0x487B60
    if msg is None: msg = await ctx.send(embed=cur)

    queue_list = await load_queue(msg)

    QUEUE_INDEX[ctx.guild.id] = 0
    if ctx.guild.id not in QUEUE_ID:  QUEUE_ID.append(ctx.guild.id)

    await msg.edit(
                    content = '', 
                    embed=await convert_queue_to_embed(ctx, queue_list, 0), 
                    view=QueueButton()
                )

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
            except Exception as e:
                print(e)
                queue[i].title = 'Error Title | Title will show by Fresh button'
                embedVar.add_field(name=f'**f[{start+i+1}]\t Error Title | Title will show by Fresh button\n**', value=f'', inline=False)
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