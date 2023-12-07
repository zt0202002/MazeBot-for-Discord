from help_functions.help_text import *
from help_functions.help_info import validate_list
from commands.music.music_playlist import player
from commands.music.cmd_play import play, play_music, check_bot_in_channel
import validators, os

async def load(ctx, path, bot, msg=None):
    msg = await check_bot_in_channel(ctx, bot, msg=msg)
    if msg == None: # not_in_same_channel
        return
    num_of_new = await player.load_json(ctx.guild.id, path)
    if num_of_new <= 0: 
        await msg.edit(content='', embed=str_no_guild_history)
        return
    await play_music(ctx, bot, msg, num_of_new)

async def load_user_list(ctx, bot):
    file = f'./QueueLog/UserPlaylist/{ctx.author.id}.json'
    if os.path.exists(file):
        with open(file, 'r') as f:
            url = f.read()
            await play(ctx, bot, url)
    else:
        await ctx.send(content='', embed=str_no_playlist)

async def save_url_user_list(ctx, url):
    if not validators.url(url):
        await ctx.send(embed=str_invalid_url)
    elif await validate_list(url):
        with open(f'./QueueLog/UserPlaylist/{ctx.author.id}.json', 'w') as f:
            f.write(url)
        embed_var = discord.Embed(title="保存了歌单捏！", description="", color=SUCCESS)
        await ctx.send(content='', embed=embed_var)
    else:
        await ctx.send(embed=str_invalid_url)

