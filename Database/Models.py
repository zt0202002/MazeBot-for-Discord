import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

Base = declarative_base()

# CREATE THE TABLE MODEL TO USE IT FOR QUERYING

class MusicSQL(Base):
    __tablename__ = 'music'
    mid = db.Column(db.Integer, primary_key = True, autoincrement =True, default = 0)
    mname = db.Column(db.String)
    mlink = db.Column(db.String)
    mtime = db.Column(db.String)

class MusicServerSQL(Base):
    __tablename__ = 'music_server'

    mid = db.Column(db.Integer, primary_key = True)
    sid = db.Column(db.String)
    cid = db.Column(db.String)
    uid = db.Column(db.String)
    
    status = db.Column(db.String, default = 'wait')
    pDate = db.Column(db.DateTime, default = datetime.now())
    startTime = db.Column(db.DateTime)

class UserSQL(Base):
    __tablename__ = 'user'
    uid = db.Column(db.String, primary_key = True)
    uname = db.Column(db.String)

class ServerSQL(Base):
    __tablename__ = 'server'
    sid = db.Column(db.String, primary_key = True)
    sname = db.Column(db.String)

class ChannelSQL(Base):
    __tablename__ = 'channel'
    cid = db.Column(db.String, primary_key = True)
    cname = db.Column(db.String)
    sid = db.Column(db.String)

class MessageSQL(Base):
    __tablename__ = 'message'
    message_id = db.Column(db.String, primary_key = True, autoincrement = True)
    sid = db.Column(db.String)
    cid = db.Column(db.String)
    uid = db.Column(db.String) 
    message = db.Column(db.String)
    message_time = db.Column(db.DateTime, default = datetime.now())

class UserLikedSQL(Base):
    __tablename__ = 'user_liked'
    mid = db.Column(db.Integer)
    uid = db.Column(db.String, primary_key = True)

class UserSavedSQL(Base):
    __tablename__ = 'user_saved'
    uid = db.Column(db.String, primary_key = True)
    ulink = db.Column(db.String)