import requests, json, discord, logging, sys, signal, asyncio, functools, typing, os
#from revChatGPT.ChatGPT import Chatbot
#from revChatGPT.Official import Chatbot
from revChatGPT.V3 import Chatbot

from os.path import exists
from dotenv import load_dotenv
from commands.music import cmd_modify, cmd_play, cmd_queue, cmd_join, cmd_current, cmd_resume

chatbot = {}
CHAT_CHANNEL_ID = []
CHAT_MUSIC_ID = []
CHAT_THREAD_ID = {}
CHAT_GID = []

def split_string_into_chunks(string, chunk_size):
  chunks = []# Create an empty list to store the chunks
  while len(string) > 0:# Use a while loop to iterate over the string
    chunk = string[:chunk_size]# Get the first chunk_size characters from the string
    chunks.append(chunk)# Add the chunk to the list of chunks
    string = string[chunk_size:]# Remove the chunk from the original string
  return chunks# Return the list of chunks

def tidy_response(i):# Optionally spoilerify or hide the most repetitive annoying nothing responses, rebrand to EvilCorp
    spoiler_bad_responses=False
    hide_bad_responses=True
    rebrand_responses=True
    bad_responses=["As a large language model trained by OpenAI,","As a language model trained by OpenAI,","My training data has a cutoff date of 2021, so I don't have knowledge of any events or developments that have occurred since then.","I'm not able to browse the internet or access any new information, so I can only provide answers based on the data that I was trained on.","I don't have the ability to provide personal opinions or subjective judgments, as I'm only able to provide objective and factual information.","I'm not able to engage in speculative or hypothetical discussions, as I can only provide information that is based on verifiable facts.","I'm not able to provide medical, legal, or financial advice, as I'm not a qualified professional in these fields.","I'm not able to engage in conversations that promote or encourage harmful or offensive behavior.","I don't have personal experiences or opinions, and I can't provide personalized advice or recommendations.","As a language model, I'm not able to perform actions or execute commands. I can only generate text based on the input I receive.","I'm not able to provide direct answers to questions that require me to make judgments or evaluations, such as questions that ask for my opinion or perspective on a topic.","I can provide information on a wide range of subjects, but my knowledge is limited to what I have been trained on and I do not have the ability to browse the internet to find new information","I do not have the ability to browse the internet or access information outside of what I have been trained on.","I'm sorry, but as a large language model trained by OpenAI, "]
    if i.find("`") == -1: # Only attempt if no code block is inside the response
        if spoiler_bad_responses:
            #bad_responses_found=[response.replace(response, "||" + response + "||") for response in bad_responses if response in i]
            bad_responses_found=[response for response in bad_responses if response in i]
            bad_responses_string = "".join(bad_responses_found)
        if hide_bad_responses:
            for br in bad_responses:i=i.replace(br, "")
        if spoiler_bad_responses and bad_responses_string != '':i+='\n||'+bad_responses_string+'||'
    if rebrand_responses:
        i=i.replace("OpenAI", "MazeCharmZzT")
        i=i.replace("!Dream:", "!dream ")
    return i

# def to_thread(func: typing.Callable) -> typing.Coroutine:
#     @functools.wraps(func)
#     async def wrapper(*args, **kwargs):
#         loop = asyncio.get_event_loop()
#         wrapped = functools.partial(func, *args, **kwargs)
#         return await loop.run_in_executor(None, wrapped)
#     return wrapper

# @to_thread
async def get_answer(chatbot,query,id):
    try:
        response = await asyncio.wait_for(asyncio.to_thread(chatbot.ask,query,user=id), timeout=60)
    except asyncio.TimeoutError:
        return "Timeout!"
    return response
    """
    prev_text = ""
    for data in chatbot.ask(query):
        print('str indicies: ', data)
        message = data["message"][len(prev_text):]
        print(message, end="", flush=True)
        prev_text = data["message"]
    return prev_text
    """
    

async def load_channel_id(bot):
    global CHAT_CHANNEL_ID, CHAT_MUSIC_ID, CHAT_GID, CHAT_THREAD_ID
    chat_file = f'./QueueLog/ChatGPTChannel/chatchannel.json'
    music_file = f'./QueueLog/ChatGPTChannel/chatmusic.json'
    gid_file = f'./QueueLog/ChatGPTChannel/chatserver.json'
    thread_file = f'./QueueLog/ChatGPTChannel/chatthread.json'

    # load channel id
    if exists(chat_file):
        try:    
            with open(chat_file, 'r') as f:  CHAT_CHANNEL_ID = json.load(f)
        except: CHAT_CHANNEL_ID = []
    else:
        with open(chat_file, 'w') as f:  json.dump([], f)

    # load music channel id
    if exists(music_file):
        try: 
            with open(music_file, 'r') as f:  CHAT_MUSIC_ID = json.load(f)
        except:
            CHAT_MUSIC_ID = []
    else:
        with open(music_file, 'w') as f:  json.dump([], f)

    # load server id
    if exists(gid_file):
        try: 
            with open(gid_file, 'r') as f:  CHAT_GID = json.load(f)
        except:
            CHAT_GID = []
    else:
        with open(gid_file, 'w') as f:  json.dump([], f)

    # load thread id
    if exists(thread_file):
        try:    
            with open(thread_file, 'r') as f:  CHAT_THREAD_ID = json.load(f)
            delete_list = []
            for i in CHAT_THREAD_ID:    
                if bot.get_channel(int(i)) is None:  
                    print('Thread Deleted: ', i)
                    delete_list.append(i)
            for i in delete_list:   del CHAT_THREAD_ID[i]
            with open(thread_file, 'w') as f:  json.dump(CHAT_THREAD_ID, f)
        except:
            CHAT_THREAD_ID = {}
    else:
        with open(thread_file, 'w') as f:  json.dump({}, f)

async def set_channel(cid, type='chat'):
    global CHAT_CHANNEL_ID, CHAT_MUSIC_ID, CHAT_GID, CHAT_THREAD_ID

    if type == 'chat':
        if cid in CHAT_CHANNEL_ID:  return '聊天频道'
        elif cid in CHAT_MUSIC_ID:  return '音乐频道'

    if type == 'chat':  file = f'./QueueLog/ChatGPTChannel/chatchannel.json'
    elif type == 'music':  file = f'./QueueLog/ChatGPTChannel/chatmusic.json'
    elif type == 'server':  file = f'./QueueLog/ChatGPTChannel/chatserver.json'
    else:   return
    
    with open(file, 'r') as f: 
        try:    CHAT_ID = json.load(f)
        except: CHAT_ID = []

        if cid not in CHAT_ID:  CHAT_ID.append(cid)

        if type=='chat':   
            CHAT_CHANNEL_ID = CHAT_ID
            with open(file, 'w') as f: json.dump(CHAT_CHANNEL_ID, f)
        elif type=='music':
            CHAT_MUSIC_ID = CHAT_ID
            with open(file, 'w') as f: json.dump(CHAT_MUSIC_ID, f)
        elif type=='server':
            CHAT_GID = CHAT_ID
            with open(file, 'w') as f: json.dump(CHAT_GID, f)

    return '设置成功'

async def remove_channel(cid, type='chat'):
    global CHAT_CHANNEL_ID, CHAT_MUSIC_ID, CHAT_GID, CHAT_THREAD_ID
    if type == 'chat':  file = f'./QueueLog/ChatGPTChannel/chatchannel.json'
    elif type == 'music':  file = f'./QueueLog/ChatGPTChannel/chatmusic.json'
    elif type == 'server':  file = f'./QueueLog/ChatGPTChannel/chatserver.json'
    elif type == 'thread':  file = f'./QueueLog/ChatGPTChannel/chatthread.json'
    else:   return
    
    with open(file, 'r') as f: 
        # CHAT_CHANNEL_ID = json.load(f)
        if cid in CHAT_CHANNEL_ID and type=='chat':
            if len(CHAT_CHANNEL_ID) == 1:   CHAT_CHANNEL_ID = []
            else:                           CHAT_CHANNEL_ID.remove(cid)
            with open(file, 'w') as f:      json.dump(CHAT_CHANNEL_ID, f)
        elif cid in CHAT_MUSIC_ID and type=='music':
            if len(CHAT_MUSIC_ID) == 1:     CHAT_MUSIC_ID = []
            else:                           CHAT_MUSIC_ID.remove(cid)
            with open(file, 'w') as f:      json.dump(CHAT_MUSIC_ID, f)
        elif cid in CHAT_GID and type=='server':
            if len(CHAT_GID) == 1:          CHAT_GID = []
            else:                           CHAT_GID.remove(cid)
            with open(file, 'w') as f:      json.dump(CHAT_GID, f)
        elif type=='thread':
            if str(cid.id) in CHAT_THREAD_ID:
                if len(CHAT_THREAD_ID) == 1:    CHAT_THREAD_ID = dict()
                else:                           del CHAT_THREAD_ID[str(cid.id)]
                with open(file, 'w') as f:      json.dump(CHAT_THREAD_ID, f)
                await cid.delete()
            else:
                await cid.delete()


async def turn_on_chatgpt(gid, prompt=None, thread_prompt=None, thread_customized=None):
    load_dotenv()
    global chatbot
    key = os.getenv('CHATGPT_API_KEY')
    # print(f'{key}')
    if prompt is None:
        with open('chatgpt_prompts/dcbot_prompt.prompt', 'r') as file:  prompt = file.read()
        chatbot[gid] = Chatbot(api_key=key, max_tokens=3096, system_prompt=prompt)
        await set_channel(gid, 'server')
    elif prompt == 'music':
        with open('chatgpt_prompts/dcbot_music.prompt', 'r') as file:
            prompt = file.read()
        chatbot[gid] = Chatbot(api_key=key, max_tokens=2048, system_prompt=prompt)
        return
    elif prompt == 'thread':
        if thread_customized is None:
            with open('chatgpt_prompts/dcbot_prompt.prompt', 'r') as file:  prompt = file.read()
        elif thread_prompt is None:
            prompt = thread_customized
        else:
            # TODO: add thread prompt
            pass
        chatbot[gid] = Chatbot(api_key=key, max_tokens=3096, system_prompt=prompt)

async def turn_off_chatgpt(gid):
    global chatbot, CHAT_GID
    # print(CHAT_GID)
    if gid in CHAT_GID:  
        chatbot[gid] = None
        await remove_channel(gid, 'server')
    # return chatbot

def clear_previous_chat_history(chatbot):
    if chatbot.get_max_tokens('default') > 1536: return
    chat_len = len(chatbot.conversation['default'])
    if chat_len <= 1:   return
    try:
        for i in range(chat_len):
            if chatbot.get_max_tokens('default') <= 1536:
                chatbot.conversation['default'].pop(1)
    except:
        return

async def is_music_commands(ctx, bot, msg, response):
    global chatbot
    # check if the message is a music command
    if ('\\') not in response:   return False

    print(response)

    # check valid commands
    if '\play' == response.split(' ')[0]:
        url = response.split(' ')[1]
        await cmd_play.play(ctx, bot, url, msg=msg)
    elif '\join' == response:
        await cmd_join.join(ctx, bot, msg=msg)
    elif '\queue' == response:
        await cmd_queue.queue(ctx, bot, msg)
    elif '\current' == response:
        await cmd_current.current(ctx, bot, msg, True)
    elif '\\resume' == response:
        await cmd_resume.resume(ctx, bot, msg=msg)
    elif '\search' == response.split(' ')[0] and len(response.split(' ')) > 1:
        content = response.split(' ')[1]
        await cmd_play.search(ctx, bot, content, msg=msg)
    elif '\pause' in response:
        await cmd_resume.pause(ctx, bot, msg=msg)
    elif '\skip' in response:
        await cmd_modify.skip(ctx, bot, msg=msg)
    elif '\leave' in response:
        await cmd_join.leave(ctx, bot, msg=msg)
    else:
        return False


    music_gpt = chatbot['music']
    music_gpt.reset()
    return True

async def set_thread(ctx, bot, name, prompt, type = 'public'):
    global chatbot, CHAT_THREAD_ID
    file = f'./QueueLog/ChatGPTChannel/chatthread.json'
    # if channel is thread
    if ctx.channel.type == discord.ChannelType.public_thread or ctx.channel.type == discord.ChannelType.private_thread:
        # print(CHAT_THREAD_ID)
        thread = ctx.channel
        await ctx.reply('Change the name of the thread to start a new chat.')
        await thread.edit(name=name)
        if thread.id not in CHAT_THREAD_ID: 
            CHAT_THREAD_ID[str(thread.id)] = prompt
            await thread.edit(name=name)

    elif type == 'public':  thread = await ctx.channel.create_thread(name=name, type=discord.ChannelType.public_thread)
    elif type == 'private': thread = await ctx.channel.create_thread(name=name, type=discord.ChannelType.private_thread)
    else:                   await ctx.reply('What the hell you got here?');   return

    await thread.send(f'This is a thread with chatgpt. The prompt:\n ```\n{prompt}\n```')
    if type == 'public':    await ctx.reply(f'Created a thread with chatgpt!\n{thread.mention}')
    else:                   await ctx.reply(f'Created a private thread with chatgpt!\n{thread.mention}', ephemeral=True)

    # add thread id to json
    with open(file, 'r') as f:  CHAT_THREAD_ID = json.load(f)
    CHAT_THREAD_ID[str(thread.id)] = prompt
    with open(file, 'w') as f:  json.dump(CHAT_THREAD_ID, f)

    # turn on chatgpt
    await turn_on_chatgpt(str(thread.id), prompt="thread", thread_prompt=None, thread_customized=prompt)