from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from commands.music.music_playlist import player

# 跳过所有歌曲
async def skipall(ctx, bot):
    msg = await ctx.send(embed=str_skiping_song)
    voice = get(bot.voice_clients, guild=ctx.guild)
    gid = ctx.guild.id

    if voice.is_playing(): voice.stop()
    player.clear(gid)
    await msg.edit(content = '', embed=str_no_song_next)

# 跳过数首歌到指定的歌曲
async def skipto(ctx, index, bot, needs_msg=True):
    try:    index = int(index)
    except: await ctx.send(embed=str_invalid_number)

    if needs_msg:
        msg = await ctx.send(embed=str_skiping_song)
    voice = get(bot.voice_clients, guild=ctx.guild)
    gid = ctx.guild.id
    playlist = player.get_list(gid)
    curr_info = player.get_curr(gid)
    
    if playlist == [] or curr_info == {}:
        embed_var = str_no_song_playing
    elif index <= 0 or index > len(playlist) + 1:
        embed_var = str_invalid_number  
    else: # 0 < num_of_skip < 待播放 + 正在播放
        if voice.is_playing(): voice.stop()
        player.remove_list(gid, index-1)
        player.play(ctx)
        curr_info = player.get_curr(gid)
        desc = f'{curr_info["title"]}\n{curr_info["webpage_url"]}'
        embed_var = discord.Embed(title=f'我来播放这首歌了捏', description=desc, color=SUCCESS)
        
    if needs_msg: await msg.edit(content='', embed=embed_var)




# 跳过正在播放的歌曲
async def skip(ctx, bot, msg=None):
    await skipto(ctx, 1, bot, needs_msg = msg==None)



# 正在播放：当前号
# [1]      列表1号
# [2]      列表2号
# [3]      列表3号
# [4]      列表4号
# [5]      列表5号
# [6]      列表6号

# skipto列表第3首，index = 3
# 跳过正在播放和列表2首，num_of_remove = index-1 = 2
# player.play()，播放列表3号