from help_functions.help_text import *
from help_functions.help_time import *
from discord import FFmpegPCMAudio
from os.path import exists
from yt_dlp import YoutubeDL
from pytube import Playlist, YouTube as yt
from bilibili_api import video as bilibili_video

import json 

song_queue = {}
current_song = {}

async def addToQueue(guild, ctx=None, url = None):
    global song_queue
    global current_song

    if guild.id not in song_queue:
        song_queue[guild.id] = []

    if 'youtube' not in url and 'bilibili' not in url:
        try:
            with YoutubeDL(YDL_OPTIONS) as ydl: info = ydl.extract_info(url, download=False)
            count = 0
            if 'entries' in info:
                for i in info['entries']:
                    song_queue[guild.id].append(i)
                    count += 1
                return count
            else:
                song_queue[guild.id].append(info)
                return 1
        except:
            return False
    elif 'bilibili' in url:
        try:
            # Get the video id
            bv = None
            p = None
            for i in url.split('&')[0].split('/'):
                if 'BV' in i:   
                    if '?p=' in i:
                        bv = i.split('?p=')[0]
                        p = i.split('?p=')[1]
                    else:
                        bv = i
                    break
            if bv == None:  return False

            # Get the video url
            link = 'https://www.bilibili.com/video/' + bv

            # Get the video info
            v = bilibili_video.Video(bvid=bv)
            info = await v.get_info()
            video_num = info['videos']
            videos = info['pages']

            # Add the video to the queue
            if p is not None:
                temp_info = {'title': videos[int(p)-1]['part'], 'url': link + '?p=' + p}
                song_queue[guild.id].append(temp_info)
                return 1
            
            for i in range(video_num):
                temp_info = {'title': videos[i]['part'], 'url': link + '?p=' + str(i+1)}
                song_queue[guild.id].append(temp_info)
                print(temp_info)
            return video_num
        except Exception:
            print(Exception)
            return False
    else:
        try:
            playlist = Playlist(url)
            assert len(playlist.videos) > 0
            for video in playlist.videos:
                song_queue[guild.id].append(video)
            return len(playlist.videos)
        except:
            try:
                video = yt(url)
                song_queue[guild.id].append(video)
                return 1
            except:
                return False
    # else:
    #     try:
    #         if "entries" in song:
    #             for i in song['entries']:
    #                 song_queue[guild.id].append(i)
    #         else:
    #             song_queue[guild.id].append(song)
    #         return 1
    #     except:
    #         return False

def check_queue(ctx, id):
    if song_queue[id] != []:
        voice = ctx.guild.voice_client
        if len(song_queue[id]) == 0:    return None
        elif not voice:                 return None
        else:
            while True:
                try:
                    cur_info = song_queue[id].pop(0)
                    try:    url = cur_info.watch_url
                    except: url = cur_info['url']
                    with YoutubeDL(YDL_OPTIONS) as ydl: info = ydl.extract_info(url, download=False)
                    break
                except:
                    continue

            temp = {}; temp['info'] = info; temp['time'] = datetime.now();  temp['status'] = 'playing'
            temp['pauseTime'] = -1
            current_song[id] = temp
            URL = info['url']
            source = FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)
            voice.play(source, after=lambda x=0: check_queue(ctx, id))
    else:
        current_song[id] = {}
        return None

async def save_queue_into_file(voice, id, path='ServerHistory'):
    file = f'./QueueLog/{path}/{id}.json'
    
    if id not in song_queue:
        song_queue[id] = []
        current_song[id] = {}
        
    elif len(song_queue[id]) > 0 or current_song[id] != {}:
        temp_urls = []
        temp_urls.append(current_song[id]['info']['webpage_url'])
        for i in song_queue[id]:    
            try:    temp_urls.append(i.watch_url)
            except: temp_urls.append(i['url'])
        
        with open(file, 'w') as f:  json.dump(temp_urls, f)
        for i in range(len(song_queue)):  song_queue[id].pop(0)
        current_song[id] = {}
        
        return True
    else:
        song_queue[id] = []
        current_song[id] = {}

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
