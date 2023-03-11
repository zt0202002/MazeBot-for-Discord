import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from Database.Models import MusicSQL, UserSQL, ServerSQL
from help_functions.help_text import *
from youtube_dl import YoutubeDL
import os
from pytube import Playlist

class song:
    def __init__(self, id = None, name = None, url = None, time = None):
        self.id, self.name, self.url, self.time = id, name, url, time

    def load(self, s):
        self.id, self.name, self.url, self.time = s.mid, s.mname, s.mlink, s.mtime
        return self

class user:
    def __init__(self, uid = None, uname = None, db = None):
        self.db = db
        if uname == None:
            user_exist = self.db.get_user_by_id(uid)
            if user_exist:
                self.uid, self.uname = user_exist.uid, user_exist.uname
            else:
                self.uname = None
        else:
            self.uid, self.uname, self.db = uid, uname, db
            user_exist = self.db.get_user_by_id(uid)
            if not user_exist:  self.db.add_user(uid, uname)

    def get_queue(self, sid, type):
        temp_queue = []
        result = self.db.get_user_queue(self.uid, sid, type)
        for r in result:
            s = self.db.get_music_by_id(r.mid)
            temp_queue.append(song().load(s))
        return temp_queue

    def get_wait_queue_server(self, sid):  return self.get_queue(sid, 'wait')
    def get_history_queue_server(self, sid):   return self.get_queue(sid, 'played')
    def get_all_queue_server(self, sid):   return self.get_queue(sid, 'all')
    def get_all_queue(self):    return self.get_queue(None, None)

class server:
    def __init__(self, server_name = None, server_id = None, db = None):
        self.db = db
        if server_name == None: 
            server_exist = self.db.get_server_by_id(server_id)
            if server_exist:
                self.sname, self.sid, self.db = server_exist.sname, server_exist.sid, db
            else:
                self.sname = None
        else:
            self.sname, self.sid, self.db = server_name, server_id, db
            server_exist = self.db.get_server_by_id(server_id)
            if not server_exist:    self.db.add_server(server_id, server_name)

    def add_song(self, uid, cid, url):
        with YoutubeDL(YDL_OPTIONS) as ydl: cur_info = ydl.extract_info(url, download=False)
        if not cur_info:    return False
        cur_song = song(name = cur_info['title'], url =cur_info['webpage_url'], time = cur_info['duration'])
        print(f'title: {cur_song.name}, time: {cur_song.time}, url: {cur_song.url}')
        self.db.add_music(uid, cid, self.sid, cur_song.name, cur_song.url, cur_song.time)
        return cur_song

    async def add_song_to_queue(self, uid, cid, playlist):
        c = 0
        for video in playlist.videos:
            # with YoutubeDL(YDL_OPTIONS) as ydl: cur_info = ydl.extract_info(video.watch_url, download=False)
            # cur_song = song(name = cur_info['title'], url =cur_info['webpage_url'], time = cur_info['duration'])
            # print(f'title: {cur_song.name}, time: {cur_song.time}, url: {cur_song.url}')
            self.db.add_music(uid, cid, self.sid, video.title, video.watch_url, -1, False)
            c += 1
        self.db.session.commit()
        return c

    def get_queue_len(self, type):
        result = self.db.get_server_queue(self.sid, type)
        return result.count()

    def get_queue(self, type):
        temp_queue = []
        result = self.db.get_server_queue(self.sid, type)
        for r in result: 
            s = self.db.get_song_by_id(r.mid)
            temp_queue.append(song(s.mid, s.mname, s.mlink, s.mtime))
        return temp_queue
    
    def play_first_song(self):
        self.db.play_first_song(self.sid)
        return self.get_playing_song()

    def get_playing_song(self):
        playing_song = song()
        playing_song.load(self.db.get_playing_song(self.sid))
        return playing_song

    def add_time_to_cur_playing_song(self, time):
        self.db.add_time_to_cur_playing_song(self.sid, time)

    def mark_first_song_played(self):
        if self.check_song_in_play():
            self.db.mark_first_song_played(self.sid)

    def check_song_in_play(self):
        return self.db.check_song_in_play(self.sid)    

    def get_last_song(self):
        last_song = song()
        last_song.load(self.db.get_last_song(self.sid))
        return last_song

    def delete_song(self, pos):
        return self.db.remove_music_pos(self.sid, pos)

    def get_wait_queue(self):   return self.get_queue('wait')
    def get_history_queue(self):    return self.get_queue('history')
    def get_all_queue(self): return self.get_queue('all')

class channel:
    def __init__(self, channel_name = None, channel_id = None, server_id = None, db = None):
        self.db = db
        if channel_name == None:
            channel_exist = self.db.get_channel_by_id(channel_id)
            if channel_exist:
                self.cname, self.cid, self.sid, self.db = channel_exist.cname, channel_exist.cid, channel_exist.sid, db
            else:
                self.cname = None
        else:
            self.sname, self.cid, self.sid, self.db = channel_name, channel_id, server_id, db
            channel_exist = self.db.get_channel_by_id(channel_id)
            if not channel_exist:
                self.db.add_channel(channel_id, channel_name, server_id)
                print('channel not in db')