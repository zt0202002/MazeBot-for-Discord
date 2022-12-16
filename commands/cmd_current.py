from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from help_functions.help_queue import *

async def current(ctx, bot):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if ctx.guild.id not in current_song or not voice.is_playing() or current_song[ctx.guild.id] == {}:
        await ctx.send(embed=str_not_song_playing)
    else:
        current = current_song[ctx.guild.id]['info']
        timer = check_time(current_song[ctx.guild.id])
        embedVar = discord.Embed(title=f'当前播放:\n{current["title"]} [{timer[0]}/{timer[1]}]', description=f'{current["webpage_url"]}', color=0x487B60)
        await ctx.send(embed=embedVar)