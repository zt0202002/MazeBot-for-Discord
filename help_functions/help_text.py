import discord

YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
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

str_not_in_voice_channel = discord.Embed(title="你都不在频道！你让我来干嘛！快输入/join让我来你的频道！", description="", color=0xD0B8A0)
str_not_in_same_channel = discord.Embed(title="我都不在你的频道！你让我来干嘛！快输入/join让我来你的频道！", description="", color=0xD0B8A0)
str_no_netease = discord.Embed(title="目前不支持网易云捏!", description="", color=0xD0B8A0)
str_join_channel = discord.Embed(title="我来你的频道啦！快让我康康你", description="", color=0x487B60)
str_loading_song = discord.Embed(title=f'加载歌曲ing...', description='', color=0x8B4C39)
str_not_song_playing = discord.Embed(title=f'我没有要播放的歌了捏！', description='', color=0x487B60)
str_exceds_songs = discord.Embed(title=f'我没有那么多歌播放捏！', description='', color=0x487B60)
str_no_song_next = discord.Embed(title=f'接下来我没有要播放的歌了捏！', description='', color=0x487B60)
str_not_playlist = discord.Embed(title=f'这不是一个播放列表捏！', description='', color=0x487B60)
str_invalid_url = discord.Embed(title=f'这不是一个有效的链接捏！', description='', color=0x487B60)