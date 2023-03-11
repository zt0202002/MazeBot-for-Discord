from Database.baseclass import *
from Database.database import *

db = None

def initialize_db():
    global db
    db = musicdb()

class DBloader:
    global db
    def __init__(self):
        self.db = db

    def load_server(self, sid):
        return server(server_id = sid, db = db)
    
    def load_user(self, uid):
        return user(uid = uid, db = db)
    
    def load_channel(self, cid):
        return channel(channel_id = cid, db = db)

    def load_all(self, ctx):
        sid = ctx.guild.id
        sname = ctx.guild.name
        cid = ctx.channel.id
        cname = ctx.channel.name
        uid = ctx.author.id
        uname = ctx.author.name

        self.server = server(sname, sid, db)
        self.channel = channel(cname, cid, sid, db)
        self.user = user(uid, uname, db)