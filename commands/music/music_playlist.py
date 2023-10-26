from discord import FFmpegPCMAudio
from help_functions.help_info import create_info
from datetime import datetime



class Player():
    def __init__(self):
        self.list = {}
        self.curr = {}

    def clear(self, gid):
        self.list[gid] = []
        self.curr[gid] = {}



    def play(self, ctx):
        gid = ctx.guild.id
        voice = ctx.guild.voice_client
        
        if not voice or self.list[gid] == [] or len(self.list[gid]) == 0:
            self.curr[gid] = {}
            return None
        
        info = self.set_curr(gid, self.list[gid].pop(0), "[正在播放]", start=datetime.now(), pause=None)
        # source = FFmpegPCMAudio(info['webpage_url'], **FFMPEG_OPTIONS) # ubuntu
        source = FFmpegPCMAudio("testaudio.m4a") # ???
        voice.play(source, after=lambda e: self.play(ctx))
    


    def get_curr(self, gid):
        if gid in self.curr:
            return self.curr[gid]
        return {}

    def set_curr(self, gid, info, status, start, pause):
        info["start"] = start
        info["pause"] = pause
        info["status"] = status #[正在播放] 或[已暂停]
        self.curr[gid] = info
        return info



    def get_list(self, gid):
        if gid in self.list:
            return self.list[gid]
        return []

    async def add_list(self, gid, url):
        if gid not in self.list:
            self.list[gid] = []
        new_info = await create_info(url)
        if new_info is None: 
            return 0
        else:
            self.list[gid] += new_info
            return len(new_info)
    
    def remove_list(self, gid, num_of_remove):
        if gid not in self.list: return
        if num_of_remove <= 0:   return

        if num_of_remove >= len(self.list[gid]) + 1:
            self.clear(gid)
        else:
            self.curr[gid] = {}
            self.list[gid] = self.list[gid][num_of_remove:]
            # list = [1,2,3,4,5]
            # list[2:] -> [3,4,5]
        
        

player = Player()