# 接受一个url，返回一个带有类youtubeDL格式的dict（见备注）

from typing import List, Dict, Union
import asyncio, pytz
from datetime import datetime
from help_functions.help_text import *
from yt_dlp import YoutubeDL
from pytube import YouTube, Playlist
import bilibili_api.video as bilibili_video
import bilibili_api.channel_series as bilibili_list
from bilibili_api.utils.short import get_real_url
from urllib.parse import urlparse, parse_qs



# YoutubeDL key备注
{
    "webpage_url":  "链接",
    "title":        "文件标题",
    "id":           "BV号, 必要时可以去重",
    "extractor":    "文件来源(YouTube, BiliBili, NetEase, etc.)",
    "duration":     "以秒计的时长(int)",
    "uploader":     "上传者",
    "thumbnail":    "封面",
    "download":     "未下载/正在下载/已下载/放弃下载",
    "filename":     "gid-extractor-id.m4a"
}



async def create_info(url: str, time_str: str) -> List[Dict[str, Union[str, int, 下载状态]]]:
    # b站短链
    if 'b23.tv' in url:
        long_url = await get_real_url(url)
        return await bilibili_info(long_url, time_str)
    # b站
    elif 'bilibili.com' in url:
        return await bilibili_info(url, time_str)
    # YouTube
    elif 'youtube.com' in url or 'youtu.be' in url:
        loop = asyncio.get_event_loop()
        info_list = await loop.run_in_executor(None, youtube_info, url, time_str)
        return info_list
    # 网易云，SoundCloud，Bandcamp，etc.
    else:
        loop = asyncio.get_event_loop()
        info_list = await loop.run_in_executor(None, others_info, url, time_str)
        return info_list



async def bilibili_info(url: str, time_str: str) -> List[Dict[str, Union[str, int, 下载状态]]]:
    url_parsed = urlparse(url)
    path = url_parsed.path

    # 单集视频，合集视频（多p）
    if 'video' in path:
        # /video/BVxxxxxxxxxx/ => ['','video','BVxxxxxxxxxx','']
        bv = path.split('/')[2]
        return await bilibili_video_info(bv, time_str)
    
    # 合集/列表
    elif 'space.bilibili.com' in url_parsed.netloc:
        try:
            # '/00000000/channel/seriesdetail' => ['','00000000', 'channel', 'seriesdetail']
            user_id = int(path.split('/')[1])
            query = parse_qs(url_parsed.query)
            list_id = int(query["sid"][0])
            # 合集（高级收藏夹，看起来像分p）
            if 'seriesdetail' in path:
                list_type = bilibili_list.ChannelSeriesType.SERIES
            # 列表（自定义收藏夹）
            elif 'collectiondetail' in path:
                list_type = bilibili_list.ChannelSeriesType.SEASON # 怀疑名字之后会改
            else: return None
            # 获取合集/列表，转为单链接视频的list
            pl = bilibili_list.ChannelSeries(uid=user_id, type_=list_type, id_=list_id)
            playlist = await pl.get_videos()
            bv_list = map(lambda video: video["bvid"], playlist['archives'])
            info_list = await asyncio.gather(*map(lambda bv: bilibili_video_info(bv, time_str), bv_list))
            
            # python拍平list的黑魔法（二维变一维
            return [info for sublist in info_list for info in sublist]
            
        # 无关的个人空间链接
        except: return []
    # 其他b站链接
    else: return []

# 读取bilibili-api的信息，转成类youtubeDL返回
# 分开写主要是为了分隔title的写法
async def bilibili_video_info(bv: str, time_str: str) -> List[Dict[str, Union[str, int, 下载状态]]]:
    try:
        v = bilibili_video.Video(bvid=bv)
        info = await v.get_info()
        if info["videos"] == 1: # 单集(单p)
            return [{
                'webpage_url':  f'https://www.bilibili.com/video/{bv}',
                'title':        f'{info["title"]}',
                'id':           bv,
                'extractor':    'BiliBili',
                'duration':     info["duration"],
                'uploader':     info["owner"]["name"],
                'thumbnail':    info["pic"],
                'download':     下载状态.未下载,
                'filename':     f'BiliBili-{bv}-{time_str}.m4a'
            }]
        else: # 合集(多p)
            return list(map(lambda page: {
                'webpage_url':  f'https://www.bilibili.com/video/{bv}?p={page["page"]}',
                'title':        f'<{info["title"][:20]}>  {page["part"]}',
                'id':           f'{bv}?p={page["page"]}',
                'extractor':    'BiliBili',
                'duration':     page["duration"],
                'uploader':     info["owner"]["name"],
                'thumbnail':    info["pic"],
                'download':     下载状态.未下载,
                'filename':     f'BiliBili-{bv}-{page["page"]}p-{time_str}.m4a'
            }, info["pages"]))
    except: return []





def youtube_info(url: str, time_str: str) -> List[Dict[str, Union[str, int, 下载状态]]]:
    # 合集
    try:
        playlist = Playlist(url)
        assert len(playlist.videos) > 0
        info_list = []
        for info in playlist.videos:
            try:
                #info.check_availability() # raise exception
                info_list.append({
                    'webpage_url':  info.watch_url,
                    'title':        info.title,
                    'id':           info.video_id,
                    'extractor':    'youtube',
                    'duration':     info.length,
                    'uploader':     info.author,
                    'thumbnail':    info.thumbnail_url,
                    'download':     下载状态.未下载,
                    'filename':     f'youtube-{info.video_id}-{time_str}.m4a'
                })
            except e: print(e)
        return info_list
    # 单个视频
    except Exception as e:
        try:
            info = YouTube(url)
            #info.check_availability() # raise exception
            return [{
                'webpage_url':  info.watch_url,
                'title':        info.title,
                'id':           info.video_id,
                'extractor':    'youtube',
                'duration':     info.length,
                'uploader':     info.author,
                'thumbnail':    info.thumbnail_url,
                'download':     下载状态.未下载,
                'filename':     f'youtube-{info.video_id}-{time_str}.m4a'
            }]
        except: return []



def others_info(url: str, time_str: str) -> List[Dict[str, Union[str, int, 下载状态]]]:
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl: info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            return list(map(lambda page: {
                'webpage_url':  page['webpage_url'],
                'title':        page['title'],
                'id':           page['id'],
                'extractor':    page['extractor'],
                'duration':     page['duration'],
                'uploader':     page['uploader'],
                'thumbnail':    page['thumbnail'],
                'download':     下载状态.未下载,
                'filename':     f'{page["extractor"]}-{page["id"]}-{time_str}.m4a'
            }, info['entries']))
        else:
            return [{
                'webpage_url':  info['webpage_url'],
                'title':        info['title'],
                'id':           info['id'],
                'extractor':    info['extractor'],
                'duration':     info['duration'],
                'uploader':     info['uploader'],
                'thumbnail':    info['thumbnail'],
                'download':     下载状态.未下载,
                'filename':     f'{info["extractor"]}-{info["id"]}-{time_str}.m4a'
            }]
    except: return []