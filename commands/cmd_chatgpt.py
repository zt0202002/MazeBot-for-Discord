import requests, json, discord, logging, sys, signal, asyncio, functools, typing, os
#from revChatGPT.ChatGPT import Chatbot
#from revChatGPT.Official import Chatbot
from revChatGPT.V3 import Chatbot

from dotenv import load_dotenv
from commands import cmd_play, cmd_queue, cmd_join, cmd_current, cmd_resume, cmd_search, cmd_skip

chatbot = {}

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
    response = chatbot.ask(query,user=id)
    return response
    prev_text = ""
    for data in chatbot.ask(query):
        print('str indicies: ', data)
        message = data["message"][len(prev_text):]
        print(message, end="", flush=True)
        prev_text = data["message"]
    return prev_text


async def turn_on_chatgpt(gid, prompt=None):
    load_dotenv()
    global chatbot
    key = os.getenv('CHATGPT_API_KEY')
    # print(f'{key}')
    if prompt is None:
        with open('chatgpt_prompts/dcbot_prompt.prompt', 'r') as file:
            prompt = file.read()
    if prompt == 'music':
        with open('chatgpt_prompts/dcbot_music.prompt', 'r') as file:
            prompt = file.read()
        chatbot[gid] = Chatbot(api_key=key, max_tokens=2048, system_prompt=prompt)
        return
    chatbot[gid] = Chatbot(api_key=key, max_tokens=3096, system_prompt=prompt)

def turn_off_chatgpt(gid):
    global chatbot
    chatbot[gid] = None
    # return chatbot

def clear_previous_chat_history(chatbot):
    if chatbot.get_max_tokens('default') > 1024: return
    chat_len = len(chatbot.conversation['default'])
    for i in range(chat_len):
        if chatbot.get_max_tokens('default') <= 1536:
            chatbot.conversation['default'].pop(1)

async def is_music_commands(ctx, bot, msg, response):
    global chatbot
    # check if the message is a music command
    if ('\\') not in response:   return False

    # check valid commands
    if '\play' in response:
        url = response.split(' ')[1]
        await cmd_play.play(ctx, url, bot, msg)
    elif '\join' in response:
        await cmd_join.join(ctx, bot, msg)
    elif '\queue' in response:
        await cmd_queue.queue(ctx, bot, msg)
    elif '\current' in response:
        await cmd_current.current(ctx, bot, msg)
    elif '\\resume' in response:
        await cmd_resume.resume(ctx, bot, msg)
    elif '\search' in response:
        content = response.split(' ', 1)[1]
        await cmd_search.search(ctx, content, bot, msg)
    elif '\pause' in response:
        await cmd_resume.pause(ctx, bot, msg)
    elif '\skip' in response:
        await cmd_skip.skip(ctx, bot, msg)
    else:
        return False

    music_gpt = chatbot['music']
    music_gpt.reset()
    return True

# async def chatgpt(msg, str):