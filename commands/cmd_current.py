from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from help_functions.help_queue import *
from discordhelp import getEmoteFromName

CURRENT_ID = []

async def current(ctx, bot, msg=None):
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
        msg = await ctx.send(embed=embedVar)
    else:
        msg = await msg.edit(content = '', embed=embedVar)
    
    if msg.id not in CURRENT_ID:
        CURRENT_ID.append(msg.id)

    await add_emoji_options(msg)
        
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