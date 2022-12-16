import discord
import os
# load our local env so we dont have the token in public
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
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

from commands import messages, test_slash, cmd_join, cmd_play, cmd_search, cmd_queue, cmd_current, cmd_delete
from commands import cmd_skip, cmd_resume, cmd_clear, cmd_report, cmd_loading

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
            self.synced = True
        print(f"We have logged in as {self.user}.")

    # async def on_command_error(self, ctx, error):
    #     await ctx.reply(error)

    

bot = Bot()

@bot.event
async def on_message(message):  await messages.on_message(message, bot)

@bot.event
async def on_voice_state_update(member, before, after): await cmd_join.on_voice_state_update(member, before, after, bot)

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

@bot.hybrid_command(with_app_command=True, name = 'load', description=dp.loading) #guild specific slash command
async def loading(ctx, *, action: Literal['Server History', 'Mine']):
    embedVar = discord.Embed(title="个人音乐及历史记录功能正在开发中...", description="Please wait...", color=0x00ff00)
    if action == 'Server History':  await cmd_loading.loading_queue(ctx, action, bot)
    elif action == 'Mine':  await cmd_loading.loading_queue(ctx, action, bot)
    else:  await ctx.send(embed = embedVar)

@bot.hybrid_command(with_app_command=True, name = 'save', description=dp.save) #guild specific slash command
async def saving(ctx, *, url: str): await cmd_loading.save_url_to_file(ctx, url, bot)

@bot.hybrid_command(with_app_command=True, name = 'clear', description=dp.clear) #guild specific slash command
# @commands.has_permissions(administrator=True)
async def clear(ctx, amount: int): 
    await ctx.send("Clearing...")
    await ctx.channel.purge(limit=amount + 1)

bot.run(os.getenv('TOKEN'))