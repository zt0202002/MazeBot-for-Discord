from help_functions.help_text import *
from help_functions.help_time import *
from commands.music.music_playlist import player

async def randomQueue(ctx):
    msg = await ctx.send(embed = str_loading_song)
    if player.shuffle_list(ctx.guild.id): 
        str_random_queue = discord.Embed(title='随机播放队列', description='队列已随机', color=SUCCESS)
    else:
        str_random_queue = discord.Embed(title='随机播放队列', description='队列太短啦，无法随机', color=FAILURE)
    await msg.edit(embed=str_random_queue)