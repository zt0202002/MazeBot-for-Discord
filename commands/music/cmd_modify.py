from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from commands.music.music_playlist import player

# 跳过所有歌曲
async def skipall(ctx, bot):
    msg = await ctx.send(embed=str_skiping_song)
    voice = get(bot.voice_clients, guild=ctx.guild)
    gid = ctx.guild.id

    voice.stop()
    await player.clear(gid)
    await msg.edit(content = '', embed=str_no_song_next)

# 跳过数首歌到指定的歌曲
async def skipto(ctx, index, bot, needs_msg=True):
    if needs_msg:
        msg = await ctx.send(embed=str_skiping_song)
    voice = get(bot.voice_clients, guild=ctx.guild)
    gid = ctx.guild.id
    playlist = player.get_list(gid)
    curr_info = player.get_curr(gid)
    
    if curr_info == {}:
        embed_var = str_no_song_playing
    elif playlist == []: # 最后一首
        voice.stop()
        embed_var = str_no_song_next
    elif index <= 0 or index > len(playlist) + 1:
        embed_var = str_invalid_number
    else: # 1 <= index <= 待播放总数
        voice.stop()
        skipped = await player.skip_to_list(gid, index-1)
        if skipped:
            await player.play(ctx, bot)
            curr_info = player.get_curr(gid)
            desc = f'{curr_info["title"]}\n{curr_info["webpage_url"]}'
            embed_var = discord.Embed(title=f'我来播放这首歌了捏', description=desc, color=SUCCESS)
        else:
            embed_var = str_no_song_playing
        
    if needs_msg: await msg.edit(content='', embed=embed_var)




# 跳过正在播放的歌曲
async def skip(ctx, bot, index=None, msg=None):
    if index is None:
        await skipto(ctx, 1, bot, needs_msg = msg==None)
    else:
        await skipat(ctx, index)



async def skipat(ctx, index):
    deleted_elem = await player.delete_list_elem(ctx.guild.id, index-1)
    if deleted_elem is None:
        embed_var = str_no_search_result
    else:
        embed_var = discord.Embed(title=f'我把第{index}首歌删掉了捏！', description=f'{deleted_elem["title"]}', color=SUCCESS)
    await ctx.send(embed=embed_var)



async def top(ctx, index):
    top_elem = player.move_top_list(ctx.guild.id, index-1)
    if top_elem is None:
        embed_var = str_no_search_result
    else:
        embed_var = discord.Embed(title=f'我把第{index}首歌置顶了捏！', description=f'{top_elem["title"]}', color=SUCCESS)
    await ctx.send(embed=embed_var)



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