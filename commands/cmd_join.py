from discord.utils import get
from help_functions.help_text import *
from help_functions.help_queue import *

async def join(ctx, bot):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await ctx.defer(ephemeral=True)
    await ctx.reply(embed=str_join_channel)

async def leave(ctx, bot):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await save_queue_into_file(voice, ctx.guild.id)
        await voice.disconnect()
        await ctx.send('我走啦！')
        song_queue[ctx.guild.id] = []
        current_song[ctx.guild.id] = {}
    else:
        await ctx.send("我不在语音频道捏！")

async def on_voice_state_update(member, before, after, bot):
    if (after.channel and len(after.channel.members) == 1):
        voice = before.channel.guild.voice_client
        await save_queue_into_file(voice, after.channel.guild.id)
        if voice: await voice.disconnect()
        else: print('voice is None')
        song_queue[after.channel.guild.id] = []
        current_song[after.channel.guild.id] = {}
        return
    elif (before.channel and len(before.channel.members) == 1):
        voice = before.channel.guild.voice_client
        await save_queue_into_file(voice, before.channel.guild.id)
        if voice: await voice.disconnect()
        else: print('voice is None before')
        song_queue[before.channel.guild.id] = []
        current_song[before.channel.guild.id] = {}
        return