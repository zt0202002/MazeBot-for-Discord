from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from help_functions.help_queue import *
from discordhelp import getEmoteFromName
from commands.cmd_resume import *
from commands.cmd_skip import *

CURRENT_ID = []

class CurrentButton(discord.ui.View):

    @discord.ui.button(label="Play | Paus", row=0, style=discord.ButtonStyle.primary)
    async def resume_button_callback(self, interaction, button):
        button = await resume(interaction, interaction.client, interaction.message)
        if button is False: await pause(interaction, interaction.client, interaction.message)
        # await asyncio.sleep(0.5)
        embedvar = await current(interaction, interaction.client, interaction.message)
        await interaction.response.edit_message(content = '', embed=embedvar, view=self)

    @discord.ui.button(label="Skip", row=0, style=discord.ButtonStyle.primary)
    async def skip_button_callback(self, interaction, button):
        await skip(interaction, interaction.client, interaction.message)
        # await asyncio.sleep(0.5)
        embedvar = await current(interaction, interaction.client, interaction.message)
        await interaction.response.edit_message(content = '', embed=embedvar, view=self)

    @discord.ui.button(label="Load", row=0, style=discord.ButtonStyle.success)
    async def refresh_button_callback(self, interaction, button):
        embedvar = await current(interaction, interaction.client, interaction.message)
        await interaction.response.edit_message(content = '', embed=embedvar, view=self)

async def current(ctx, bot, msg=None, gpt=False):
    voice = get(bot.voice_clients, guild=ctx.guild)
    # if ctx.guild.id not in current_song or (not voice.is_playing() or current_song[ctx.guild.id] == {}:
    if ctx.guild.id not in current_song or current_song[ctx.guild.id] == {}:
        embedVar = str_not_song_playing
    else:
        current = current_song[ctx.guild.id]['info']
        timer = check_time(current_song[ctx.guild.id])
        status = "正在播放" if current_song[ctx.guild.id]['status'] == 'playing' else "已暂停"
        embedVar = discord.Embed(title=f'当前播放:\n{current["title"]} [{timer[0]}|{timer[1]}] [{status}]', description=f'{current["webpage_url"]}', color=0x487B60)
    
    if msg is None:
        msg = await ctx.send(embed=embedVar, view=CurrentButton())
    if gpt and msg is not None:
        await msg.edit(content = '', embed=embedVar, view=CurrentButton())

    return embedVar

    if msg is None:
        msg = await ctx.send(embed=embedVar, view=CurrentButton())
    else:
        msg = await msg.edit(content = '', embed=embedVar, view=CurrentButton())
    
    if msg.id not in CURRENT_ID:
        CURRENT_ID.append(msg.id)

    # await add_emoji_options(msg)
        
async def add_emoji_options(msg):
    await msg.clear_reactions()

    pause = getEmoteFromName(":pause_button:")
    play = getEmoteFromName(":arrow_forward:")
    skip = getEmoteFromName(":track_next:")
    refresh = getEmoteFromName(":arrows_counterclockwise:")

    await msg.add_reaction(pause)
    await msg.add_reaction(play)
    await msg.add_reaction(skip)
    await msg.add_reaction(refresh)