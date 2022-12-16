import random

######### Bot Commands #########
# @bot.event
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
    
    elif "捏" in user_message:      await message.channel.send('捏')
    
    elif ("吗" in user_message or "嘛" in user_message) and random_reply_q == 3:
        reply_msg = user_message.replace("吗", "啊").replace("嘛", "啊").replace("？", "！")
        
        if "你" in reply_msg:       reply_msg = reply_msg.replace("你", "我")
        elif "我" in reply_msg:     reply_msg = reply_msg.replace("我", "你")
        await message.channel.send(reply_msg)
    
    elif ("?" in user_message or "？" in user_message) and random_reply_q == 10:    await message.channel.send('?')
    
    elif "我要" in user_message and random_reply_b == 1:    await message.channel.send('我绰！别！')
    
    elif ("原" in user_message or "O" in user_message or "p" in user_message or "P" in user_message or "o" in user_message):
        if "Tony" in username and random_reply_o == 1:     await message.channel.send('我绰！有OP！')
    
    await bot.process_commands(message)
##################################