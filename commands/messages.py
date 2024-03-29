import random
from discord.utils import get
# from commands.speech_synthesis import tts
import discord
import time

import importlib
import commands.speech_synthesis

from commands.cmd_chatgpt import *
import commands.cmd_chatgpt as chatgpt

import requests, json, discord, logging, sys, signal, asyncio, functools, typing, os

on_tts = False
userdb={}

######### Bot Commands #########
# @bot.event
async def on_message(message, bot, interaction=None):
    if message.author == bot.user: return
    # print(chatgpt.CHAT_CHANNEL_ID)

    if message.guild is None:
        await bot.process_commands(message)
        return
    if message.content.startswith('\\') or message.content.startswith('、'):
        await bot.process_commands(message)
        return
    
    # initialize music bot gpt

    gid = message.guild.id
    did = message.channel.id
    chatbot = chatgpt.chatbot

    if 'music' not in chatbot:    await turn_on_chatgpt('music', 'music')
    
    if message.content.startswith('.') or message.content.startswith('。') or message.channel.id in chatgpt.CHAT_MUSIC_ID:
        music_chat_bot = chatgpt.chatbot['music']
        await send_gpt_msg(message, bot, music_chat_bot)
        return
    
    if message.channel.type == discord.ChannelType.private_thread or message.channel.type == discord.ChannelType.public_thread:
        thread = message.channel
        thread_id = str(thread.id)

        if thread_id in chatgpt.CHAT_THREAD_ID and thread_id not in chatbot:
            await turn_on_chatgpt(thread_id, 'thread', None, chatgpt.CHAT_THREAD_ID[thread_id])

        if thread_id in chatbot and chatbot[thread_id] is not None:
            await send_gpt_msg(message, bot, chatbot[thread_id])
            return
    
    if gid in chatgpt.CHAT_GID and gid not in chatbot:
        await turn_on_chatgpt(gid)
    elif gid not in chatbot or chatbot[gid] is None:
        if message.content.startswith(';;on'):
            await message.channel.send('Starting chatbot...')
            await turn_on_chatgpt(gid)
            return
        else:
            await bot.process_commands(message)
            return
    chatbot = chatbot[gid]

    if message.content.startswith(';;on'):
        await message.channel.send('Chatbot is already on...')
        return
    elif message.content.startswith(';;off'):
        await message.channel.send('Chatbot is off...')
        await turn_off_chatgpt(gid)
        return
    elif message.content.startswith(';;reset'):
        await message.channel.send('Resetting chatbot...')
        chatbot.reset()
        return
    elif message.content.startswith(';;pop'):
        await message.channel.send('Populating chatbot...')
        if len(chatbot.conversation['default']) > 1:
            chatbot.conversation['default'].pop(1)
        return
    elif message.content.startswith(';;show'):
        await message.channel.send('Showing chatbot...')
        print(chatbot.conversation['default'])
        return
    elif message.content.startswith(';;tokens'):
        await message.channel.send(f'Showing tokens... [{chatbot.get_token_count()}]')
        return
    elif message.content.startswith(';;maxtokens'):
        default = 'default'
        await message.channel.send(f'Showing max tokens... [{chatbot.get_max_tokens(default)}]')
        return
    # if message.channel.id != config["discord_channel"] and type(message.channel)!=discord.DMChannel: return
    
    if message.author.bot:
        await bot.process_commands(message)
        return
    
    # print(message.channel.id)
    # if ((message.channel.id != 1084285046220918864 and message.channel.id != 1084883338873032704 and message.channel.id != 1084945212029276242 and message.channel.id != 1085348253039603772)
    
    if ((did not in chatgpt.CHAT_CHANNEL_ID)
        and not message.content.startswith('!') and not message.content.startswith('！')
        and not message.content.startswith(';') and not message.content.startswith('；')): 
    
        await bot.process_commands(message)
        return
    
    if (message.content.startswith('!') or message.content.startswith('！')
        or message.content.startswith(';') or message.content.startswith('；')):
            
        message.content = message.content[1:]
        
    # if message.content == '!refresh': chatbot.refresh_session(); await message.add_reaction("🔄"); print("refresh session"); return
    # if message.content == '!restart' and message.author.id == config['discord_admin_id']: os.execl(__file__, *sys.argv);return
    if message.content == '!reset': chatbot.reset();await message.add_reaction("💪"); print("reset chat"); return
    if message.content.startswith('\\') or message.content.startswith('、'):
        await bot.process_commands(message)
        return
    
    longquery=''
    if message.attachments and message.attachments[0].width and message.attachments[0].height:
        #image_url = message.attachments[0].proxy_url
        #image_desc = extract_text_from_image_url(image_url)
        #longquery=await message.reply(image_desc)
        return
    if message.attachments and message.attachments[0].content_type.startswith('text'):
        print('text attachment found, adding to prompt')
        attachment=message.attachments[0]
        data=await attachment.read()
        longquery=data.decode()
    # if message.mentions:
    #     for user in message.mentions:
    #         if user != client.user: return
    print(message.author.name+':'+message.content)

    await send_gpt_msg(message, bot, chatbot, longquery)

async def send_gpt_msg(message, bot, cb, longquery=''):
    try:
        did=str(message.channel.id)

        clear_previous_chat_history(cb)
        msg = await message.reply('Thinking...')
        query=message.content
        if longquery and longquery != '':
            query=message.content+'\n```'+longquery+'\n```'

        else:#In channel
            async with message.channel.typing():
                if message.content.startswith('.') or message.content.startswith('。'):
                    response=await get_answer(chatbot['music'],query,did)
                else:
                    response=await get_answer(cb,query,did)

        if await is_music_commands(message, bot, msg, response):  return

        r=tidy_response(response)
        chunks=split_string_into_chunks(r,1975) # Make sure response chunks fit inside a discord message (max 2k characters)
        for chunk in chunks:
            if chunk == chunks[0]:  await msg.edit(content=chunk)
            else:  await message.channel.send(chunk)
            
    except Exception as e:
        print("Something went wrong!")
        error=(str(e))
        #if error == "'NoneType' object is not subscriptable":
        #if error == "('Response code error: ', 429)":
        #    error+='\nPlease wait for your previous response to be answered before asking another'
        if error == "('Response code error: ', 403)":
            error+='\n403 forbidden response from api server'
        if error == "('Response code error: ', 524)":
            error+='\nHTTP response status code 524 A timeout occurred is an unofficial server error that is specific to Cloudflare. This HTTP status code occurs when a successful HTTP connection was made to the origin server but the HTTP Connection timed out before the HTTP request was complete'
        if error == "('Response code error: ', 502)":
            error+='\nHTTP response status code 502 Bad Gateway server error response code indicates that the server, while acting as a gateway or proxy, received an invalid response from the upstream server.'
        errorembed=discord.Embed(description=':warning: '+error, color=0xFF5733)
        await message.reply(embed=errorembed)
        await message.add_reaction("💩")

        print('====================')
        print(error)
        print('====================')

    # await bot.process_commands(message)

'''
async def on_message(message, bot):
    if message.author == bot.user: return

    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'[{channel}] {username}: {user_message}')

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
'''
##################################