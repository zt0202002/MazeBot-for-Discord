import random
from discord.utils import get
from commands.speech_synthesis import tts
import discord
import time

import importlib
import commands.speech_synthesis

on_tts = False

######### Bot Commands #########
# @bot.event
async def on_message(message, bot):
    if message.author == bot.user: return

    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'[{message.author.name}][{channel}] {username}: {user_message}')

    random_reply_q = random.randint(1, 100)
    random_reply_b = random.randint(1, 100)
    random_reply_o = random.randint(1, 100)

    if (random_reply_q == 1):       await message.channel.send('?')
    
    elif (random_reply_q == 2):     await message.channel.send('为什么呀')
    
    elif "你好" in user_message:
        if username == 'MRTx':      await message.channel.send('哇！这不是梅老师吗！')
        elif 'Nancy' in username:   await message.channel.send('哇哦！这不是南希不露吗！')
        elif 'Maze' in username:    await message.channel.send('哇哦！爹！')
        else:                       await message.channel.send('我不认识你')
    
    # elif "捏" in user_message:      await message.channel.send('捏')
    
    elif ("吗" in user_message or "嘛" in user_message) and random_reply_q == 3:
        reply_msg = user_message.replace("吗", "啊").replace("嘛", "啊").replace("？", "！")
        
        if "你" in reply_msg:       reply_msg = reply_msg.replace("你", "我")
        elif "我" in reply_msg:     reply_msg = reply_msg.replace("我", "你")
        await message.channel.send(reply_msg)
    
    elif ("?" in user_message or "？" in user_message) and random_reply_q == 10:    await message.channel.send('?')
    
    elif "我要" in user_message and random_reply_b == 1:    await message.channel.send('我绰！别！')
    
    elif ("原" in user_message or "O" in user_message or "p" in user_message or "P" in user_message or "o" in user_message):
        if "Tony" in username and random_reply_o == 1:     await message.channel.send('我绰！有OP！')

    if on_tts:
        voice = get(bot.voice_clients, guild=message.guild)
        if voice and voice.is_connected():
            importlib.reload(commands.speech_synthesis)
            from commands.speech_synthesis import tts

            if (await tts(message)):
                voice.play(discord.FFmpegPCMAudio("/Users/taozhang/Desktop/My Porjects/MazeBot-for-Discord/voices/test.mp3"))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.5
                while voice.is_playing():
                    time.sleep(1)
                voice.stop()
                # os.remove("/Users/taozhang/Desktop/My Porjects/MazeBot-for-Discord/test.mp3")
                return

    await bot.process_commands(message)
##################################