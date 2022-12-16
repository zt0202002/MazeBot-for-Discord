from help_functions.help_text import *
from help_functions.help_time import *
from discord import FFmpegPCMAudio
from os.path import exists
from youtube_dl import YoutubeDL

import json 

song_queue = {}
current_song = {}

async def addToQueue(guild, song, ctx=None):
    if guild.id not in song_queue:
        song_queue[guild.id] = []

    if "entries" in song:
        for i in song['entries']:
            song_queue[guild.id].append(i)
    else:
        song_queue[guild.id].append(song)

def check_queue(ctx, id):
    if song_queue[id] != []:
        voice = ctx.guild.voice_client
        if len(song_queue[id]) == 0:
            return None
        elif not voice:
            return None
        else:
            info = song_queue[id].pop(0)
            temp = {}; temp['info'] = info; temp['time'] = datetime.now()
            current_song[id] = temp
            URL = info['url']
            source = FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)
            voice.play(source, after=lambda x=0: check_queue(ctx, id))
    else:
        return None

async def save_queue_into_file(voice, id, path='ServerHistory'):
    file = f'./QueueLog/{path}/{id}.json'
    
    if id not in song_queue:
        song_queue[id] = []
    elif len(song_queue[id]) > 0 or (voice and (voice.is_playing() and current_song[id] != {})):
        song_queue[id].insert(0, current_song[id]['info'])
        with open(file, 'w') as f:
            json.dump(song_queue[id], f)
    else:
        with open(file, 'w') as f:
            json.dump([], f)

async def load_queue_from_file(guild, path='ServerHistory', user_id=None):
    id = guild.id
    file = f'./QueueLog/{path}/{id}.json'
    if user_id: file = f'./QueueLog/{path}/{user_id}.json'

    song_len = 0

    if id not in song_queue:
        song_queue[id] = []

    if exists(file):
        with open(file, 'r') as f:
            if path=='ServerHistory':
                json_queue = f.read()
                saved_queue = json.loads(json_queue)
                if saved_queue != [] and saved_queue[0] != {}:
                    song_queue[id].extend(saved_queue)
                    song_len = len(saved_queue)
            elif path == "UserPlaylist":
                url = f.read()
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                if "entries" in info:
                    await addToQueue(guild, info)
                    song_len = len(info['entries'])
    
    return song_len
