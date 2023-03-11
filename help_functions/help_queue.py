from help_functions.help_text import *
from help_functions.help_time import *
from discord import FFmpegPCMAudio
from os.path import exists
from youtube_dl import YoutubeDL
from pytube import Playlist, YouTube as yt
from Database.dbloader import *

import json 

song_queue = {}
current_song = {}

async def addToQueue(ctx, url):
    dbloader = DBloader()
    dbloader.load_all(ctx)
    server = dbloader.server
    channel = dbloader.channel
    user = dbloader.user

    print(server.sname)

    # playlist = Playlist(url)
    # c = 0
    # for video in playlist.videos:
    #     print('title: ' + video.title + ', url: ' + video.watch_url)
    #     server.add_song(user.uid, channel.cid, video.watch_url)
    #     c += 1
    # return c

    try:
        playlist = Playlist(url)
        c = await server.add_song_to_queue(user.uid, channel.cid, playlist)
        return c
    except:
        try:
            print('~')
            server.add_song(user.uid, channel.cid, url)
            return 1
        except:
            return False

# async def addToQueue(guild, ctx=None, url = None):
#     if guild.id not in song_queue:
#         song_queue[guild.id] = []

#     try:
#         playlist = Playlist(url)
#         for video in playlist.videos:
#             song_queue[guild.id].append(video)
#         return len(playlist.videos)
#     except:
#         try:
#             video = yt(url)
#             song_queue[guild.id].append(video)
#             return 1
#         except:
#             return False
#     # else:
#     #     try:
#     #         if "entries" in song:
#     #             for i in song['entries']:
#     #                 song_queue[guild.id].append(i)
#     #         else:
#     #             song_queue[guild.id].append(song)
#     #         return 1
#     #     except:
#     #         return False

def check_queue(ctx, id):
    if song_queue[id] != []:
        voice = ctx.guild.voice_client
        if len(song_queue[id]) == 0:    return None
        elif not voice:                 return None
        else:
            cur_info = song_queue[id].pop(0)
            with YoutubeDL(YDL_OPTIONS) as ydl: info = ydl.extract_info(cur_info.watch_url, download=False)

            temp = {}; temp['info'] = info; temp['time'] = datetime.now()
            current_song[id] = temp
            URL = info['url']
            source = FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)
            voice.play(source, after=lambda x=0: check_queue(ctx, id))
    else:
        current_song[id] = {}
        return None

def play_first_song(voice):
    dbloader = DBloader()
    server = dbloader.load_server(voice.guild.id)

    try:
        server.mark_first_song_played()
        song = server.play_first_song()
        
        with YoutubeDL(YDL_OPTIONS) as ydl: cur_info = ydl.extract_info(song.url, download=False)
        source = FFmpegPCMAudio(cur_info['url'], **FFMPEG_OPTIONS)
        voice.play(source, after=lambda x=0: play_first_song(voice))

        print('Playing: ' + cur_info['title'], cur_info['duration'])
        server.add_time_to_cur_playing_song(voice.guild.id, cur_info['duration'])
        song.time = cur_info['duration']

        return song
    except:
        return False
    

    # return cur_info

async def save_queue_into_file(voice, id, path='ServerHistory'):
    file = f'./QueueLog/{path}/{id}.json'
    
    if id not in song_queue:
        song_queue[id] = []
    elif len(song_queue[id]) > 0 or current_song[id] != {}:
        temp_urls = []
        temp_urls.append(current_song[id]['info']['webpage_url'])
        for i in song_queue[id]:    temp_urls.append(i.watch_url)
        
        with open(file, 'w') as f:  json.dump(temp_urls, f)

        return True
    else:
        with open(file, 'w') as f:  json.dump([], f)
        return True

async def load_queue_from_file(guild, path='ServerHistory', user_id=None):
    id = guild.id
    file = f'./QueueLog/{path}/{id}.json'
    if user_id: file = f'./QueueLog/{path}/{user_id}.json'

    song_len = 0

    if id not in song_queue:    song_queue[id] = []

    if exists(file):
        with open(file, 'r') as f:
            if path=='ServerHistory':
                json_queue = f.read()
                saved_queue = json.loads(json_queue)
                if saved_queue != []:
                    for i in saved_queue:   await addToQueue(guild, url=i)
                    song_len = len(saved_queue)
            elif path == "UserPlaylist":
                url = f.read()
                song_len = await addToQueue(guild, url=url)
                # with YoutubeDL(YDL_OPTIONS) as ydl:
                #     info = ydl.extract_info(url, download=False)
                # if "entries" in info:
                #     await addToQueue(guild, info)
                #     song_len = len(info['entries'])
    
    return song_len
