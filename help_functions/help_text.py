import discord

YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s.m4a',
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