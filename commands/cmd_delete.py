from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from help_functions.help_queue import *

async def delete(ctx, index, bot):
    if ctx.guild.id not in song_queue:
        await ctx.send(embed=str_not_song_playing)
    elif len(song_queue[ctx.guild.id]) < index:
        await ctx.send(embed=str_exceds_songs)  
    else:
        info = song_queue[ctx.guild.id].pop(index-1)
        embedVar = discord.Embed(title=f'我把第{index}首歌删掉了捏！', description=f'{info["title"]}\n{info["webpage_url"]}', color=0x487B60)
        await ctx.send(embed=embedVar)