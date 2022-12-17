from help_functions.help_text import *
from help_functions.help_time import *
from help_functions.help_queue import *
import random

async def randomQueue(ctx, bot):
    msg = await ctx.send(embed = str_loading_song)
    random.shuffle(song_queue[ctx.guild.id])
    str_random_queue = discord.Embed(title='随机播放队列', description='队列已随机', color=0x487B60)
    await msg.edit(embed=str_random_queue)