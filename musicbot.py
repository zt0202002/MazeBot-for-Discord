import discord
import os, shutil
# load our local env so we dont have the token in public
from dotenv import load_dotenv
from discord.ext import commands
import description as dp
from typing import Literal

from help_functions.help_text import TEMP_AUDIO_FOLDER_NAME

from commands.music import cmd_join, cmd_modify, cmd_play, cmd_current, cmd_resume, cmd_queue, cmd_load
from commands import messages, test_slash, cmd_report, cmd_chatgpt, cmd_minecraft, cmd_googlesearch, cmd_splatoon

load_dotenv()
if os.path.exists(TEMP_AUDIO_FOLDER_NAME):
    shutil.rmtree(TEMP_AUDIO_FOLDER_NAME)
intents = discord.Intents.all()

######### Slash Commands #########
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(intents = intents, command_prefix=';')
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            # await self.tree.sync(guild = discord.Object(id=ids[0])) #guild specific: leave blank if global (global registration can take 1-24 hours)
            # await self.tree.sync(guild = discord.Object(id=ids[1])) #guild specific: leave blank if global (global registration can take 1-24 hours)
            await self.tree.sync()
            await cmd_chatgpt.load_channel_id(self)
            self.synced = True
            
        print(f"We have logged in as {self.user}.")

    # async def on_command_error(self, ctx, error):
    #     await ctx.reply(error)

    

bot = Bot()

# 音乐部分
@bot.hybrid_command(with_app_command=True, name = 'join', description=dp.join)
async def join(ctx: commands.Context):  await cmd_join.join(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'leave', description=dp.leave)
async def leave(ctx: commands.Context): await cmd_join.leave(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'quit', description=dp.leave)
async def leave(ctx: commands.Context): await cmd_join.leave(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'play', description=dp.play)
async def play(ctx: commands.Context, search_or_url: str=None): await cmd_play.play(ctx, bot, search_or_url)

@bot.hybrid_command(with_app_command=True, name = 'add', description=dp.play)
async def play(ctx: commands.Context, search_or_url: str): await cmd_play.play(ctx, bot, search_or_url)

@bot.hybrid_command(with_app_command=True, name = 'nowplaying', description=dp.current)
async def current(ctx: commands.Context): await cmd_current.current(ctx)

@bot.hybrid_command(with_app_command=True, name = 'current', description=dp.current)
async def current(ctx: commands.Context): await cmd_current.current(ctx)

@bot.hybrid_command(with_app_command=True, name = 'resume', description=dp.resume)
async def resume(ctx: commands.Context): await cmd_resume.resume(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'unpause', description=dp.resume)
async def resume(ctx: commands.Context): await cmd_resume.resume(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'pause', description=dp.pause)
async def pause(ctx: commands.Context): await cmd_resume.pause(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'stop', description=dp.pause)
async def pause(ctx: commands.Context): await cmd_resume.pause(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'skipall', description=dp.skipall)
async def skipall(ctx: commands.Context): await cmd_modify.skipall(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'skipto', description=dp.skipto)
async def skipto(ctx: commands.Context, index: int): await cmd_modify.skipto(ctx, index, bot)

@bot.hybrid_command(with_app_command=True, name = 'skip', description=dp.skip)
async def skip(ctx: commands.Context, index: int=None):  await cmd_modify.skip(ctx, bot, index)

@bot.hybrid_command(with_app_command=True, name = 'top', description=dp.top)
async def top(ctx: commands.Context, index: int):  await cmd_modify.top(ctx, index)

@bot.hybrid_command(with_app_command=True, name = 'queue', description=dp.queue)
async def queue(ctx: commands.Context): await cmd_queue.queue(ctx)

@bot.hybrid_command(with_app_command=True, name = 'playlist', description=dp.queue)
async def queue(ctx: commands.Context): await cmd_queue.queue(ctx)

@bot.hybrid_command(with_app_command=True, name = 'list', description=dp.queue)
async def queue(ctx: commands.Context): await cmd_queue.queue(ctx)

@bot.hybrid_command(with_app_command=True, name = 'search', description=dp.queue)
async def search(ctx: commands.Context, keywords: str): await cmd_play.search(ctx, bot, keywords)

@bot.hybrid_command(with_app_command=True, name = 'delete', description=dp.delete)
async def delete(ctx: commands.Context, index: int): await cmd_modify.skipat(ctx, index)

@bot.hybrid_command(with_app_command=True, name = 'random', description=dp.random)
async def random(ctx):  await cmd_modify.randomQueue(ctx)

@bot.hybrid_command(with_app_command=True, name = 'load', description=dp.load)
async def load(ctx, *, action: Literal['ServerHistory', 'Mine']):
    if action == 'ServerHistory':
        await cmd_load.load(ctx, 'ServerHistory', bot)
    elif action == 'Mine':
        await cmd_load.load_user_list(ctx, bot)
    else:
        await ctx.send(embed = discord.Embed(title="现在就两个功能捏...", description="Please wait...", color=0x00ff00))

@bot.hybrid_command(with_app_command=True, name = 'save', description=dp.save)
async def saving(ctx, *, url: str): await cmd_load.save_url_user_list(ctx, url)

# 播放音乐之外的功能
@bot.event
async def on_message(message):  await messages.on_message(message, bot)

@bot.hybrid_command(with_app_command=True, name = 'test', description='testing')
# @commands.has_permissions(administrator=True)
async def test(ctx: commands.Context): await test_slash.slash2(ctx)

@bot.hybrid_command(with_app_command=True, name = 'maze', description=dp.maze)
async def maze(ctx):    await ctx.send("http://mazecharm.notion.site")

@bot.hybrid_command(with_app_command=True, name = 'report', description=dp.report)
async def report(ctx, message: str):    await cmd_report.report(ctx, message, bot)

@bot.hybrid_command(with_app_command=True, name = 'minecraft', description=dp.minecraft)
async def minecraft(ctx): await cmd_minecraft.server_status(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'tts', description=dp.tts)
async def on_tts(ctx, *, text: str): 
    messages.on_tts = not messages.on_tts 
    await ctx.send("开启嘴替功能！")

@bot.hybrid_command(with_app_command=True, name = 'clear', description=dp.clear)
# @commands.has_permissions(administrator=True)
async def clear(ctx, amount: int): 
    await ctx.send("Clearing...")
    await ctx.channel.purge(limit=amount + 1)

@bot.hybrid_command(with_app_command=True, name = 'chatgpt_on', description=dp.chatgpton)
async def chatgpt_on(ctx):
    await cmd_chatgpt.turn_on_chatgpt(ctx.guild.id)
    await ctx.send("开启聊天功能！")

@bot.hybrid_command(with_app_command=True, name = 'chatgpt_off', description=dp.chatgptoff)
async def chatgpt_off(ctx):
    await cmd_chatgpt.turn_off_chatgpt(ctx.guild.id)
    await ctx.send("关闭聊天功能！")

@bot.hybrid_command(with_app_command=True, name = 'set_chat_channel', description=dp.chatgptChatChannel)
async def chatgpt_channel(ctx, channel: discord.TextChannel):
    result = await cmd_chatgpt.set_channel(channel.id, 'chat')
    if result != '设置成功':    
        await ctx.send(f"该频道已经被设为{result}了！")
    else:                    
        await ctx.send(f"将{channel.name}设置为聊天频道，可以和我愉快聊天啦！")

@bot.hybrid_command(with_app_command=True, name = 'set_music_channel', description=dp.chatgptMusicChannel)
async def chatgpt_channel(ctx, channel: discord.TextChannel):
    result = await cmd_chatgpt.set_channel(channel.id, 'music')
    if result != '设置成功':    
        await ctx.send(f"该频道已经被设为{result}了！")
    else:                    
        await ctx.send(f"将{channel.name}设置为音乐频道，可以和我愉快聊天啦！")
@bot.hybrid_command(with_app_command=True, name = 'delete_chat_channel', description=dp.chatgptChatChannelDelete)
async def chatgpt_channel(ctx, channel: discord.TextChannel):
    await cmd_chatgpt.remove_channel(channel.id, 'chat')
    await ctx.send(f"已关闭自动聊天功能！")

@bot.hybrid_command(with_app_command=True, name = 'delete_music_channel', description=dp.chatgptMusicChannelDelete)
async def chatgpt_channel(ctx, channel: discord.TextChannel):
    await cmd_chatgpt.remove_channel(channel.id, 'music')
    await ctx.send(f"已关闭无指令点歌功能！")

@bot.hybrid_command(with_app_command=True, name = 'chatgpt_public_thread', description=dp.chatgptPublicThread)
async def chatgpt_public_thread(ctx, name: str, prompt: str):
    await cmd_chatgpt.set_thread(ctx, bot, name, prompt, type='public')

@bot.hybrid_command(with_app_command=True, name = 'chatgpt_private_thread', description=dp.chatgptPrivateThread)
async def chatgpt_private_thread(ctx, name: str, prompt: str):
    await cmd_chatgpt.set_thread(ctx, bot, name, prompt, type='private')

@bot.hybrid_command(with_app_command=True, name = 'delete_current_thread', description=dp.chatgptDeleteThread)
async def delete_current_thread(ctx):
    if ctx.channel.type == discord.ChannelType.private_thread or ctx.channel.type == discord.ChannelType.public_thread:
        thread = ctx.channel
        await ctx.reply(f"deleting {thread.name}！")
    else:
        await ctx.reply("Current text channel is not a thread!")
        return
    # await thread.delete()
    await cmd_chatgpt.remove_channel(thread, 'thread')

@bot.hybrid_command(with_app_command=True, name = 'help_commands', description=dp.help)
async def help(ctx):
    try:
        with open('help_music.txt', 'r') as f:    help_music = f.read()
        with open('help_chatgpt.txt', 'r') as f:    help_chatgpt = f.read()
        await ctx.reply(help_music)
        await ctx.reply(help_chatgpt)
    except Exception as e:
        print(e)
        await ctx.reply("Help file not found!")

@bot.hybrid_command(with_app_command=True, name = 'server_number', description="Test Commands: show the number of servers using this bot")
async def server_number(ctx):
    await ctx.reply(f"Currently, {len(bot.guilds)} servers are using this bot!")
    names = '```\n'
    for i in bot.guilds:
        names += i.name + '\n'
    names += '```'
    await ctx.send(names)

@bot.hybrid_command(with_app_command=True, name = 'google', description='Google Search')
async def google(ctx, *, query: str):
    await ctx.interaction.response.defer(thinking=True)
    await cmd_googlesearch.google(ctx, query)

@bot.hybrid_command(with_app_command=True, name = 'reddit', description='Reddit Search')
async def google_image(ctx, *, query: str):
    await ctx.interaction.response.defer(thinking=True)
    await cmd_googlesearch.reddit(ctx, query)

@bot.hybrid_command(with_app_command=True, name = 'stackoverflow', description='Stackoverflow Search')
async def stackoverflow(ctx, *, query: str):
    await ctx.interaction.response.defer(thinking=True)
    await cmd_googlesearch.stackoverflow(ctx, query)

@bot.hybrid_command(with_app_command=True, name = 'bilibili', description='Bilibili Search')
async def bilibili(ctx, *, query: str):
    await ctx.interaction.response.defer(thinking=True)
    await cmd_googlesearch.bilibili(ctx, query)

@bot.hybrid_command(with_app_command=True, name = 'moe', description='Moe Wiki Search')
async def moe(ctx, *, query: str):
    await ctx.interaction.response.defer(thinking=True)
    await cmd_googlesearch.moe(ctx, query)

@bot.hybrid_command(with_app_command=True, name = 'ff14', description='FF14 Huiji Wiki Search')
async def ffxiv(ctx, *, query: str):
    await ctx.interaction.response.defer(thinking=True)
    await cmd_googlesearch.ffxiv(ctx, query)

@bot.hybrid_command(with_app_command=True, name = 'zhihu', description='Zhihu Search')
async def zhihu(ctx, *, query: str):
    await ctx.interaction.response.defer(thinking=True)
    await cmd_googlesearch.zhihu(ctx, query)

@bot.hybrid_command(with_app_command=True, name = 'bangumi', description='Bangumi Search')
async def bangumi(ctx, *, query: str):
    await ctx.interaction.response.defer(thinking=True)
    await cmd_googlesearch.bangumi(ctx, query)

@bot.hybrid_command(with_app_command=True, name = 'image', description='Google Image Search')
async def google_image(ctx, *, query: str):
    await ctx.interaction.response.defer(thinking=True)
    await cmd_googlesearch.image(ctx, query)

@bot.hybrid_command(with_app_command=True, name = 'gif', description='Google gif image Search')
async def google_gif(ctx, *, query: str):
    await ctx.interaction.response.defer(thinking=True)
    await cmd_googlesearch.gif(ctx, query)

@bot.hybrid_command(with_app_command=True, name = 'news', description='今日要闻')
async def news(ctx, type: Literal['World', 'Video Game']):    
    if type == 'World':
        await cmd_googlesearch.news(ctx)
    elif type == 'Video Game':
        await cmd_googlesearch.game_news(ctx)
    else:
        await ctx.reply("Invalid type!")

@bot.hybrid_command(with_app_command=True, name = 'splatoon', description='Splatoon 3 Schedule')
async def splatoon(ctx, mode: Literal['regular', 'rank', 'open_rank', 'x_rank', 'pve', 'big run', 'pve team']):
    await ctx.interaction.response.defer(thinking=True)
    await cmd_splatoon.splatoon(ctx, mode)

@bot.hybrid_command(with_app_command=True, name = 'status_set', description='Change User Status on Nickname')
async def status_set(ctx, status:str):
    member = ctx.author
    try:
        if '[' in member.nick and ']' in member.nick:
            index_0 = member.nick.index('[')
            index_1 = member.nick.index(']')

            if index_0 == 0:    nick = '[' + status + ']' + member.nick[index_1+1:]
            else:               nick = '[' + status + ']' + member.nick

        else:
            nick = '[' + status + ']' + member.nick
    except:
        nick = '[' + status + ']' + member.name

    try:
        await member.edit(nick=nick)
        await ctx.send(f'Nickname was changed for {member.mention} ')
    except:
        await ctx.send(f'Nickname was not changed for {member.mention}. Please make sure bot position is above the user.')

@bot.hybrid_command(with_app_command=True, name = 'status_remove', description='Remove User Status on Nickname')
async def status_set(ctx):
    member = ctx.author
    try:
        if '[' in member.nick and ']' in member.nick:
            index_0 = member.nick.index('[')
            index_1 = member.nick.index(']')

            if index_0 == 0:    nick = member.nick[index_1+1:]
            else:               
                await ctx.send(f'You do not have status currently.')
                return


            await member.edit(nick=nick)
            await ctx.send(f'Nickname was changed for {member.mention} ')
        else:               
            await ctx.send(f'You do not have status currently.')
            return
    except:
        await ctx.send(f'You do not have status currently.')

bot.run(os.getenv('TOKEN'))