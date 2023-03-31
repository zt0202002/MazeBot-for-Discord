import discord
import os
# load our local env so we dont have the token in public
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from yt_dlp import YoutubeDL
from discord import app_commands
from discord import opus
import description as dp
from typing import Literal

import queue, asyncio
import sys
import random

from help_functions.help_text import *
from help_functions.help_time import *
from help_functions.help_queue import *

from datetime import datetime

from concurrent.futures import ThreadPoolExecutor

from commands import messages, test_slash, cmd_join, cmd_play, cmd_search, cmd_queue, cmd_current, cmd_delete
from commands import cmd_skip, cmd_resume, cmd_clear, cmd_report, cmd_loading, cmd_random, cmd_minecraft, cmd_chatgpt
from commands import cmd_reaction

load_dotenv()
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

@bot.event
async def on_message(message):  
    # loop = asyncio.get_event_loop()
    # await asyncio.create_task(messages.on_message(message, bot))
    await messages.on_message(message, bot)

@bot.event
async def on_voice_state_update(member, before, after): await cmd_join.on_voice_state_update(member, before, after, bot)

@bot.event
async def on_reaction_add(reaction, user):  await cmd_reaction.reply_reaction(reaction, user, bot)

@bot.hybrid_command(with_app_command=True, name = 'test', description='testing') #guild specific slash command
@commands.has_permissions(administrator=True)
async def test(ctx: commands.Context): await test_slash.test(ctx)

@bot.hybrid_command(with_app_command=True, name = 'join', description=dp.join) #guild specific slash command
async def join(ctx: commands.Context):  await cmd_join.join(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'play', description=dp.play) #guild specific slash command
async def play(ctx: commands.Context, url: str): await cmd_play.play(ctx, url, bot)

@bot.hybrid_command(with_app_command=True, name = 'search', description=dp.search) #guild specific slash command
async def search(ctx: commands.Context, search: str):   await cmd_search.search(ctx, search, bot)

@bot.hybrid_command(with_app_command=True, name = 'queue', description=dp.queue) #guild specific slash command
async def queue(ctx: commands.Context): await cmd_queue.queue(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'current', description=dp.current) #guild specific slash command
async def current(ctx: commands.Context):   await cmd_current.current(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'delete', description=dp.delete) #guild specific slash command
async def delete(ctx: commands.Context, index: int):    await cmd_delete.delete(ctx, index, bot)

@bot.hybrid_command(with_app_command=True, name = 'skipall', description=dp.skipall) #guild specific slash command
async def skipall(ctx: commands.Context):  await cmd_skip.skipall(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'skipto', description=dp.skipto) #guild specific slash command
async def skipto(ctx: commands.Context, index: int):    await cmd_skip.skipto(ctx, index, bot)

@bot.hybrid_command(with_app_command=True, name = 'skip', description=dp.skip) #guild specific slash command
async def skip(ctx: commands.Context):  await cmd_skip.skip(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'resume', description=dp.resume) #guild specific slash command
async def resume(ctx: commands.Context):    await cmd_resume.resume(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'pause', description=dp.pause) #guild specific slash command
async def pause(ctx: commands.Context): await cmd_resume.pause(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'leave', description=dp.leave) #guild specific slash command
async def leave(ctx: commands.Context): await cmd_join.leave(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'maze', description=dp.maze) #guild specific slash command
async def maze(ctx):    await ctx.send("http://mazecharm.notion.site")

@bot.hybrid_command(with_app_command=True, name = 'report', description=dp.report) #guild specific slash command
async def report(ctx, message: str):    await cmd_report.report(ctx, message, bot)

@bot.hybrid_command(with_app_command=True, name = 'random', description=dp.random) #guild specific slash command
async def random(ctx):  await cmd_random.randomQueue(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'load', description=dp.loading) #guild specific slash command
async def loading(ctx, *, action: Literal['Server History', 'Mine']):
    embedVar = discord.Embed(title="现在就两个功能捏...", description="Please wait...", color=0x00ff00)
    if action == 'Server History':  await cmd_loading.loading_queue(ctx, action, bot)
    elif action == 'Mine':  await cmd_loading.loading_queue(ctx, action, bot)
    else:  await ctx.send(embed = embedVar)

@bot.hybrid_command(with_app_command=True, name = 'minecraft', description=dp.minecraft) #guild specific slash command
async def minecraft(ctx): await cmd_minecraft.server_status(ctx, bot)

@bot.hybrid_command(with_app_command=True, name = 'save', description=dp.save) #guild specific slash command
async def saving(ctx, *, url: str): await cmd_loading.save_url_to_file(ctx, url, bot)

@bot.hybrid_command(with_app_command=True, name = 'tts', description=dp.tts) #guild specific slash command
async def on_tts(ctx, *, text: str): 
    messages.on_tts = not messages.on_tts 
    await ctx.send("开启嘴替功能！")

@bot.hybrid_command(with_app_command=True, name = 'clear', description=dp.clear) #guild specific slash command
# @commands.has_permissions(administrator=True)
async def clear(ctx, amount: int): 
    await ctx.send("Clearing...")
    await ctx.channel.purge(limit=amount + 1)

@bot.hybrid_command(with_app_command=True, name = 'chatgpt_on', description=dp.chatgpton) #guild specific slash command
async def chatgpt_on(ctx):
    await cmd_chatgpt.turn_on_chatgpt(ctx.guild.id)
    await ctx.send("开启聊天功能！")

@bot.hybrid_command(with_app_command=True, name = 'chatgpt_off', description=dp.chatgptoff) #guild specific slash command
async def chatgpt_off(ctx):
    await cmd_chatgpt.turn_off_chatgpt(ctx.guild.id)
    await ctx.send("关闭聊天功能！")

@bot.hybrid_command(with_app_command=True, name = 'set_chat_channel', description=dp.chatgptChatChannel) #guild specific slash command
async def chatgpt_channel(ctx, channel: discord.TextChannel):
    await cmd_chatgpt.set_channel(channel.id, 'chat')
    await ctx.send(f"将{channel.name}设置为聊天频道，可以和我愉快聊天啦！")

@bot.hybrid_command(with_app_command=True, name = 'set_music_channel', description=dp.chatgptMusicChannel) #guild specific slash command
async def chatgpt_channel(ctx, channel: discord.TextChannel):
    await cmd_chatgpt.set_channel(channel.id, 'music')
    await ctx.send(f"将{channel.name}设置为音乐频道，可以无需指令放歌啦！")

@bot.hybrid_command(with_app_command=True, name = 'delete_chat_channel', description=dp.chatgptChatChannelDelete) #guild specific slash command
async def chatgpt_channel(ctx, channel: discord.TextChannel):
    await cmd_chatgpt.remove_channel(channel.id, 'chat')
    await ctx.send(f"已关闭自动聊天功能！")

@bot.hybrid_command(with_app_command=True, name = 'delete_music_channel', description=dp.chatgptMusicChannelDelete) #guild specific slash command
async def chatgpt_channel(ctx, channel: discord.TextChannel):
    await cmd_chatgpt.remove_channel(channel.id, 'music')
    await ctx.send(f"已关闭无指令点歌功能！")

@bot.hybrid_command(with_app_command=True, name = 'chatgpt_public_thread', description=dp.chatgptPublicThread) #guild specific slash command
async def chatgpt_public_thread(ctx, name: str, prompt: str):
    await cmd_chatgpt.set_thread(ctx, bot, name, prompt, type='public')

@bot.hybrid_command(with_app_command=True, name = 'chatgpt_private_thread', description=dp.chatgptPrivateThread) #guild specific slash command
async def chatgpt_private_thread(ctx, name: str, prompt: str):
    await cmd_chatgpt.set_thread(ctx, bot, name, prompt, type='private')

@bot.hybrid_command(with_app_command=True, name = 'delete_current_thread', description=dp.chatgptDeleteThread) #guild specific slash command
async def delete_current_thread(ctx):
    if ctx.channel.type == discord.ChannelType.private_thread or ctx.channel.type == discord.ChannelType.public_thread:
        thread = ctx.channel
        await ctx.reply(f"deleting {thread.name}！")
    else:
        await ctx.reply("Current text channel is not a thread!")
        return
    # await thread.delete()
    await cmd_chatgpt.remove_channel(thread, 'thread')

@bot.hybrid_command(with_app_command=True, name = 'help_commands', description=dp.help) #guild specific slash command
async def help(ctx):
    try:
        with open('help_music.txt', 'r') as f:    help_music = f.read()
        with open('help_chatgpt.txt', 'r') as f:    help_chatgpt = f.read()
        await ctx.reply(help_music)
        await ctx.reply(help_chatgpt)
    except Exception as e:
        print(e)
        await ctx.reply("Help file not found!")

@bot.hybrid_command(with_app_command=True, name = 'server_number', description="Test Commands: show the number of servers using this bot") #guild specific slash command
async def server_number(ctx):
    await ctx.reply(f"Currently, {len(bot.guilds)} servers are using this bot!")
    names = '```\n'
    for i in bot.guilds:
        names += i.name + '\n'
    names += '```'
    await ctx.reply(names)

bot.run(os.getenv('TOKEN2'))
