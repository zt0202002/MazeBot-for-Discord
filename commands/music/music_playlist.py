from discord import FFmpegPCMAudio
from help_functions.help_text import YDL_OPTIONS, 下载状态, MAX_DOWNLOAD_WAITING_SECONDS, TEMP_AUDIO_FOLDER_NAME
from help_functions.help_info import create_info
from datetime import datetime
import random, copy, yt_dlp, asyncio, os, pytz, json
# 下载状态文档详见help_text



class Player:
    def __init__(self):
        self._list = {}
        self._curr = {}
        self._play_count = {} # 防止skip调用skip时原play的after唤起
    
    async def guild_start(self, gid):
        # 防止上次意外退出卡死
        # 测试代码
        # if gid in self._curr:
        #     print(self._curr[gid])
        # else:
        #     print('no curr')
        # if gid in self._list:
        #     print(self._list[gid])
        # else:
        #     print('no list')
        self._list[gid] = []
        self._curr[gid] = {}

    async def clear_playlist(self, gid):
        async def clear_download(info, gid):
            if info['download'] in [下载状态.未下载, 下载状态.待下载, 下载状态.正在下载]:
                info['download'] = 下载状态.放弃下载
            elif info['download'] == 下载状态.放弃下载:
                pass
            else: # info['download'] == 下载状态.已下载
                await remove_audio(info["filename"], gid)
        
        await asyncio.gather(*map(lambda info: clear_download(info, gid), self._list[gid]))
        self._list[gid] = []
        # voice.play() after should take care of the current playing audio file
        self._curr[gid] = {}
        self._play_count[gid] = 0
    
    async def quit_save(self, gid):
        file = f'./QueueLog/ServerHistory/{gid}.json'
        if gid in self._curr and self._curr[gid] != {}:
            # 把curr变回list的一员
            del self._curr[gid]['start']
            del self._curr[gid]['pause']
            del self._curr[gid]['status']
            self._list[gid].insert(0, self._curr[gid])
            # 清除下载状态
            for info in self._list[gid]:
                info['download'] = None
            # 保存到服务器
            with open(file, 'w') as f:
                json.dump(self._list[gid], f)
        else:
            with open(file, 'w') as f:
                json.dump([], f)
        self._list[gid] = []
        self._curr[gid] = {}
    
    async def load_json(self, gid, path):
        file = f'./QueueLog/{path}/{gid}.json'
        # 读取服务器记录
        with open(file, 'r') as f:
            guild_list_save = json.load(f)
        # 加入列表
        if guild_list_save != []:
            for info in guild_list_save:
                path = os.path.join(TEMP_AUDIO_FOLDER_NAME, str(gid), info["filename"])
                # 检查下载状态
                info['download'] = 下载状态.已下载 if os.path.exists(path) else 下载状态.未下载
            # 简易版add_list
            if gid not in self._list:
                self._list[gid] = []
            self._list[gid] += guild_list_save
            # 删除服务器记录
            with open(file, 'w') as f:
                json.dump({}, f)
            return len(guild_list_save)
        else:
            return 0



    async def play(self, ctx, bot):
        gid = ctx.guild.id
        voice = ctx.guild.voice_client

        if not voice or self._list[gid] == []:
            self._curr[gid] = {}
            return
        
        if gid not in self._play_count:
            self._play_count[gid] = 1
        else: 
            self._play_count[gid] += 1
        
        # 拉取列表第一首歌信息
        info = self.set_curr(gid, self._list[gid].pop(0), "[已暂停]", start=datetime.now(), pause=datetime.now())
        # 检查这首歌是否被下载
        download_success = info['download'] == 下载状态.已下载
        if not download_success:
            if info['download'] in [下载状态.未下载, 下载状态.待下载]:
                info['download'] = 下载状态.待下载
                download_success = await asyncio.to_thread(download_audio, info, gid)
            elif info['download'] == 下载状态.正在下载: # 等一会儿下载，等不了就放弃
                    for i in range(MAX_DOWNLOAD_WAITING_SECONDS): 
                        if self._curr[gid]['download'] == 下载状态.已下载:
                            download_success = True
                        else:
                            await asyncio.sleep(1)
                    self._curr[gid]['download'] = 下载状态.放弃下载
                    download_success = False
        
        # 播放或跳到下一首
        if download_success:
            path = os.path.join(TEMP_AUDIO_FOLDER_NAME, str(gid), info["filename"])
            self.set_curr(gid, info, "[正在播放]", start=datetime.now(), pause=None)
            async def after():
                await remove_audio(info['filename'], gid)
                self._play_count[gid] -= 1
                # 还没有测试下一首歌不能播放的问题
                # print(f"count: {self._play_count[gid]} - {info['title']}")
                if self._play_count[gid] == 0:
                    await self.play(ctx, bot)
            voice.play(source=FFmpegPCMAudio(path), after=lambda _: asyncio.run_coroutine_threadsafe(after(), bot.loop))
        else:
            await self.play(ctx, bot)



    def get_curr(self, gid):
        if gid in self._curr:
            return copy.deepcopy(self._curr[gid])
        return {}

    def set_curr(self, gid, info, status, start, pause):
        info["start"] = start
        info["pause"] = pause
        info["status"] = status #[正在播放] 或 [已暂停]
        self._curr[gid] = info
        return info



    def get_list(self, gid):
        if gid in self._list:
            return copy.deepcopy(self._list[gid])
        return []

    async def add_list(self, gid, url):
        if gid not in self._list:
            self._list[gid] = []
        now = datetime.now(pytz.timezone('Etc/Greenwich'))
        time_str = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}'
        new_info = await create_info(url, time_str)
        self._list[gid] += new_info
        return len(new_info)
        
    def move_top_list(self, gid, index):
        if gid not in self._list or index < 0 or index > len(self._list[gid]): 
            return None
        self._list[gid].insert(0, self._list[gid].pop(index))
        return self._list[gid][0]
    
    async def skip_to_list(self, gid, num_of_remove):
        if gid not in self._list or num_of_remove < 0:
            return False
        elif num_of_remove >= len(self._list[gid]):
            self.clear_playlist(gid)
            return False
        else:
            # 清除列表下载。num_of_remove == 0 不受影响
            waiting_delete_list = self._list[gid][:num_of_remove]
            self._list[gid] = self._list[gid][num_of_remove:]
            for info in waiting_delete_list:
                if info['download'] in [下载状态.待下载, 下载状态.正在下载, 下载状态.未下载]:
                    info['download'] = 下载状态.放弃下载
                elif info['download'] == 下载状态.已下载:
                    await remove_audio(info["filename"], gid)
            return True
    
    async def delete_list_elem(self, gid, index):
        if index < 0 or index >= len(self._list[gid]): 
            return None
        info = self._list[gid].pop(index)
        if info['download'] == 下载状态.正在下载:
            info['download'] = 下载状态.放弃下载
        else:
            await remove_audio(info['filename'], gid)
        return info
    
    def shuffle_list(self, gid):
        random.shuffle(self._list[gid])
        return len(self._list[gid]) > 1
    
    def download_list(self, gid):
        if len(self._list[gid]) <= 0: 
            return
        waiting_download_list = list(filter(lambda info: info['download'] == 下载状态.未下载, self._list[gid]))
        for info in waiting_download_list:
            info['download'] = 下载状态.待下载
            print(f"{info['download']} {info['title']}")
        for info in waiting_download_list:
            print(f"开始下载 {info['title']}")
            audio_success = download_audio(info, gid)
            if not audio_success:
                info['download'] = 下载状态.放弃下载
                continue



def download_audio(info, gid):
    if info['download'] in [下载状态.正在下载, 下载状态.已下载]:
        return True
    elif info['download'] == 下载状态.放弃下载:
        return False
    elif info['download'] == 下载状态.待下载:
        info['download'] = 下载状态.正在下载
        try:
            download_timer = datetime.now()
            path = os.path.join(TEMP_AUDIO_FOLDER_NAME, str(gid), info['filename'])
            YDL_OPTIONS_FILENAME = {**YDL_OPTIONS, 'outtmpl': path}
            with yt_dlp.YoutubeDL(YDL_OPTIONS_FILENAME) as ydl: 
                ydl.download(info['webpage_url'])
            print(f'下载耗时: {datetime.now()-download_timer} - {info["title"]}')
        except Exception as e: 
            print(e)
            return False
        # 异步下载结束，检查下载状态是否仍为 正在下载
        path = os.path.join(TEMP_AUDIO_FOLDER_NAME, str(gid), info['filename'])
        if info['download'] == 下载状态.放弃下载 and os.path.exists(path): 
            os.remove(path)
            return False
        else:
            info['download'] = 下载状态.已下载
            return True
    else:
        # 如果是未下载，请重新检查代码逻辑。download_audio之前，download_list里就应该改成了待下载
        # 如果是其他结果，请检查info['download']赋值情形
        print(f'download_audio() exception: info[\'download\'] = {info["download"]}')
        print(f'filename: {info["title"]}')
        return False

async def remove_audio(name: str, gid: int):
    path = os.path.join(TEMP_AUDIO_FOLDER_NAME, str(gid), name)
    if os.path.exists(path): 
        for i in range(MAX_DOWNLOAD_WAITING_SECONDS):
            try:
                os.remove(path)
                break
            except: 
                await asyncio.sleep(1)



player = Player()