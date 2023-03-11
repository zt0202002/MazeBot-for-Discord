import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from Database.Models import *
import os

# Connect to Database
class musicdb:
    session = None
    def __init__(self):
        try:
            load_dotenv()
            engine = db.create_engine(f"mysql://root:{os.getenv('db_pw')}@192.168.1.176:3306/Discord_Music_Bot?charset=utf8mb4")
            Session = sessionmaker(bind=engine)
            self.session = Session()
            if self.session is not None:
                print('Database connected')
        except:
            print('Error in database.__init__')

    def add_server(self, sid, sname):
        try:
            new_server = ServerSQL(sid=sid, sname=sname)
            self.session.add(new_server)
            self.session.commit()
            return True
        except:
            print('Error in database.add_server')
            return False

    def get_server_by_id(self, sid):
        try:
            ser = self.session.query(ServerSQL).filter(ServerSQL.sid.like(sid)).first()
            return ser
        except:
            print('Error in database.get_server_by_id')
            return False

    def add_music(self, uid, cid, sid, mname, mlink, mtime, commit=True):
        # print('++++++++++++++++++')
        new_music = MusicSQL(mname=mname, mlink=mlink, mtime=mtime)
        self.session.add(new_music)
        if commit: self.session.commit()
        # print('------------------')

        mid = self.session.query(MusicSQL).order_by(MusicSQL.mid.desc()).first().mid
        # print('==================')
        # print('mid: ', mid)
        # print('sid: ', sid)
        # print('cid: ', cid)
        # print('uid: ', uid)
        new_music_server = MusicServerSQL(mid=mid, sid=sid, cid=cid, uid=uid)
        self.session.add(new_music_server)
        if commit: self.session.commit()

        return True
        # try:
        #     new_music = MusicSQL(mname=mname, mlink=mlink, mtime=mtime)
        #     self.session.add(new_music)
        #     self.session.commit()
        #     print('------------------')

        #     mid = self.session.query(MusicSQL).order_by(MusicSQL.mid.desc()).first().mid
        #     print('==================')
        #     new_music_server = MusicServerSQL(mid=mid, sid=sid, cid=cid, uid=uid)
        #     self.session.add(new_music_server)
        #     self.session.commit()

        #     return True
        # except:
        #     print('Error in database.add_music')
        #     return False

    def get_song_by_id(self, mid):
        try:
            return self.session.query(MusicSQL).filter_by(mid = mid).first()
        except:
            return False

    def add_channel(self, cid, cname, sid):
        try:
            new_channel = ChannelSQL(cid=cid, cname=cname, sid=sid)
            self.session.add(new_channel)
            self.session.commit()
            return True
        except:
            print('Error in database.add_channel')
            return False
    
    def get_channel_by_id(self, cid):
        try:
            cha = self.session.query(ChannelSQL).filter(ChannelSQL.cid.like(cid)).first()
            print(cha.cid)
            print(cid)
            return cha
        except:
            print('Error in database.get_channel_by_id')
            return False

    def play_first_song(self, sid):
        try:
            music_row = self.session.query(MusicServerSQL).filter(MusicServerSQL.sid.like(sid), 
                                                                MusicServerSQL.status.like('wait')).first()
            music_row.status = 'playing'
            music_row.isPlayed = True
            music_row.playedTime = datetime.now()
            self.session.commit()
            return True
        except:
            print('Error in database.play_first_song')
            return False

    def add_time_to_cur_playing_song(self, sid, time):
        try:
            music_row = self.session.query(MusicServerSQL).filter(MusicServerSQL.sid.like(sid), 
                                                                MusicServerSQL.status.like('playing')).first()
            music = self.session.query(MusicSQL).filter_by(mid = music_row.mid).first() 
            music.mtime = time
            self.session.commit()
            return True
        except:
            print('Error in database.add_time_to_cur_playing_song')
            return False
    
    def get_playing_song(self, sid):
        try:
            mid = self.session.query(MusicServerSQL).filter(MusicServerSQL.sid.like(sid), 
                                                                MusicServerSQL.status.like('playing')).first().mid
            return self.session.query(MusicSQL).filter_by(mid = mid).first()
        except:
            print('Error in database.get_playing_song')
            return False
    
    def get_last_song(self, sid):
        try:
            mid = self.session.query(MusicServerSQL).order_by(MusicServerSQL.mid.desc()).filter(MusicServerSQL.sid.like(sid), 
                                                            MusicServerSQL.status.like('wait')).first().mid
            return self.session.query(MusicSQL).filter_by(mid = mid).first()
        except:
            print('Error in database.get_last_song')
            return False

    def mark_first_song_played(self, sid):
        try:
            music_row = self.session.query(MusicServerSQL).filter(MusicServerSQL.sid.like(sid), 
                                                                MusicServerSQL.status.like('playing')).first()
            music_row.status = 'played'
            self.session.commit()
            return True
        except:
            print('Error in database.play_next_song')
            return False
    
    def check_song_in_play(self, sid):
        try:
            music_row = self.session.query(MusicServerSQL).filter(MusicServerSQL.sid.like(sid), 
                                                                MusicServerSQL.status.like('playing')).first()
            if music_row:
                return True
            else:
                return False
        except:
            print('Error in database.check_song_in_play')
            return False

    def get_next_song(self, sid):
        try:
            return self.session.query(MusicServerSQL).filter_by(MusicServerSQL.sid.like(sid), 
                                                                MusicServerSQL.status.like('wait')).first()
        except:
            print('Error in database.get_next_song')
            return False

    def remove_music_pos(self, sid, pos):
        try:
            music_row = self.session.query(MusicServerSQL).filter(MusicServerSQL.sid.like('sid')).offset(pos - 1).first()
            print(music_row.mid)
            self.session.query(MusicSQL).filter_by(mid = music_row.mid).delete()
            self.session.commit()
            return True
        except:
            print('Error in database.remove_music_pos')
            return False

    def add_user(self, uid, uname):
        try:
            usr = UserSQL(uid=uid, uname=uname)
            self.session.add(usr)
            self.session.commit()
        except:
            print('Error in database.add_user')
            return False
    
    def get_user_by_id(self, uid):
        try:
            usr = self.session.query(UserSQL).filter(UserSQL.uid.like(uid)).first()
            return usr
        except:
            print('Error in database.get_user_by_id')
            return False

    def get_server_queue(self, sid, type):
        try:
            if type != 'all':
                return self.session.query(MusicServerSQL).filter(MusicServerSQL.sid.like(sid), 
                                                                MusicServerSQL.status.like(type))
            else:
                return self.session.query(MusicServerSQL).filter(MusicServerSQL.sid.like(sid))
            # if type == 'wait':  music_queue = self.session.query(MusicServerSQL).filter_by(sid = sid, isPlayed = False)
            # elif type == 'history': music_queue = self.session.query(MusicServerSQL).filter_by(sid = sid, isPlayed = True)
            # elif type == 'all': music_queue = self.session.query(MusicServerSQL).filter_by(sid = sid)
            # return music_queue
        except:
            print('Error in database.get_server_queue')
            return False

    def get_user_queue(self, uid, sid, type):
        try:
            return self.session.query(MusicServerSQL).filter(MusicServerSQL.sid.like(sid),
                                                            MusicServerSQL.uid.like(uid),
                                                            MusicServerSQL.status.like(type))
            # if type == 'wait': return self.session.query(MusicServerSQL).filter_by(sid = sid, uid = uid, isPlayed = False)
            # elif type == 'history': return self.session.query(MusicServerSQL).filter_by(sid = sid, uid = uid, isPlayed = True)
            # elif type == 'all': return self.session.query(MusicServerSQL).filter_by(sid = sid, uid = uid)
            # elif sid == None and type == None: return self.session.query(MusicServerSQL).filter_by(uid = uid)
            # print('Error in database.get_user_queue')
            # return False
        except:
            print('Error in database.get_user_queue')
            return False
    
    def add_user_saved_queue(self, uid, mid):
        #   TODO:   - add a song into your saved queue
        return

    def get_user_saved_queue(self, uid, mid):
        #   TODO:   - get your saved queue
        return
