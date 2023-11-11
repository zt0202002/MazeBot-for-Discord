import discord
from enum import Enum

class 下载状态(Enum):
    # 起始情形，帮助player.download_audio()判断要不要下载
    未下载 = 0
    # 赋值：仅初始化(create_info())

    # 过程情形，帮助player.play()判断curr要不要下载，帮助如remove_audio()判断有没有未出现的删除
    正在下载 = 1
    # 赋值：player.download_audio()开头

    # 成功情形，已经有本地下载文件
    已下载 = 2
    # 赋值：player.download_audio()结尾

    # 失败情形，帮助player.download_audio()判断是否还需要下载，下载途中歌曲是否已被移除歌单
    放弃下载 = 3
    # 赋值: player.clear_download()
    #       player.skip_to_list()
    #       player.play()正在下载超时
    #       delete_list_elem()正在下载超时

YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        # 'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch',
        'source_address': '0.0.0.0',
        'max-downloads': 10
    }
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 ', 'options': '-vn'}

LOADING = 0x8B4C39
SUCCESS = 0x487B60
FAILURE = 0xD0B8A0

str_loading_bot  = discord.Embed(title=f'上线中ing...', description='', color=LOADING)
str_loading_song = discord.Embed(title=f'加载歌曲ing...', description='', color=LOADING)
str_skiping_song = discord.Embed(title=f'跳过歌曲ing...', description='', color=LOADING)

str_join_channel = discord.Embed(title="我来你的频道啦！快让我康康你", description="", color=SUCCESS)
str_leave = discord.Embed(title=f'我走啦！', description='', color=SUCCESS)
str_no_song_next = discord.Embed(title=f'接下来我没有要播放的歌了捏！', description='', color=SUCCESS)

str_not_in_voice_channel = discord.Embed(title='你都不在频道！你让我来干嘛！快输入/join让我来你的频道！', description="", color=FAILURE)
str_not_in_same_channel = discord.Embed(title='我都不在你的频道！你让我来干嘛！快输入/join让我来你的频道！', description="", color=FAILURE)
str_no_netease = discord.Embed(title="目前不支持网易云捏!", description="", color=FAILURE)


str_no_song_playing = discord.Embed(title=f'我没有要播放的歌了捏！', description='', color=FAILURE)
str_invalid_number = discord.Embed(title=f'这不是一个有效的数字捏！', description='', color=FAILURE)
str_not_playlist = discord.Embed(title=f'这不是一个播放列表捏！', description='', color=FAILURE)
str_invalid_url = discord.Embed(title=f'这不是一个有效的链接捏！', description='', color=FAILURE)
str_no_search_result = discord.Embed(title=f'没有搜索到歌捏！', description='', color=FAILURE)
str_not_in_voice = discord.Embed(title=f'我不在语音频道捏！', description='', color=FAILURE)