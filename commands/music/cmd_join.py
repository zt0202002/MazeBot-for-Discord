from discord.utils import get
from help_functions.help_text import *
from commands.music.music_playlist import player



async def join(ctx, bot, msg=None):
    try: channel = ctx.message.author.voice.channel
    except: channel = ctx.author.voice.channel

    if msg is None: msg = await ctx.send(embed=str_loading_bot)
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected(): await voice.move_to(channel)
    else:                      voice = await channel.connect()

    print(f'连接到 {ctx.guild.name} 的频道：{channel.name}')

    msg = await msg.edit(content = '', embed=str_join_channel)

    return msg



async def leave(ctx, bot, msg=None):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        if msg is None: await ctx.send(embed=str_leave)
        else:           await msg.edit(content='', embed=str_leave)
        await player.clear(ctx.guild.id)
    else:
        if msg is None: await ctx.send(embed=str_not_in_voice)
        else:           await msg.edit(content='', embed=str_not_in_voice)