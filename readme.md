# MazeBot for Discord

**添加bot：[MazeBot for Discord App](https://discord.com/oauth2/authorize?client_id=1051385856134488124&permissions=1643315723888&scope=applications.commands%20bot)**
---

> **当前版本并不稳定，可能会出现各种问题，如果有问题请联系茶慕。**

> **当前版本仅支持简单的Discord的音乐功能与聊天功能！**

> 如果使用过程中遇到任何问题，请使用 `\report` 指令向茶慕反馈问题。或者提交github issue。

### Related Links:
- **[MazeBot for Discord App](https://discord.com/api/oauth2/authorize?client_id=1051385856134488124&permissions=1643315723888&scope=applications.commands%20bot)**
- **[茶慕茶慕的Notion](https://www.notion.so/Notion-14b0d5588f804acbb39ce58bc37e978e)** 

### 联系方式：
|**平台**|**联系方式**|
|---|---|
|QQ|365968531|
|Discord|MazeCharmZzt#2964|

# Update Note
### April 12, 2023
- 将search功能放入了play这个指令中，现在可以直接用`/play <song_name>`来搜索歌曲了！
- 增加了各类信息搜索功能,详情请看下方指令列表。
- 增加了查看splatoon3地图日历的功能，详情请看下方指令列表。
- **现以支持bilibili playlist的播放！**

### March 31, 2023
- 增加了chatgpt功能！现在可以在频道里和bot聊天啦！
- 在使用`\chatgpt_on`后，支持使用`!<TEXT>`或者`;<TEXT>`和bot在频道中聊天！
- 在使用`\set_chat_channel <channel>`后，支持直接与bot在设定中的频道聊天！
- 在使用`\set_music_channel <channel>`后，支持直接用口头化的指令在设定中的频道播放音乐！
- 在使用`\chatgpt_public_thread <thread_name> <prompt>`后，支持在Thread中用自己给bot的设定进行聊天！

### December 16, 2022

- 规划整理了下当前的代码文件，将各个function写入单独的python文件中。
- 当bot所在频道没人的时候，bot会自动离开。
- 当bot离开时，保存当前未完成播放的歌单，并下次回来后输入`/load History` 即可播放之前未完成播放的歌单。

### December 14, 2022

- 现在输入`/current` 和`/queue` 能够显示当前歌曲播放的时间了!
- 现在输入`/leave` 指令能够让bot离开语音频道了！
- 现在输入`/maze` 指令能够获取茶慕的profile了！
- 现在输入`/report` 指令能够报告错误给茶慕了！

### December 13, 2022

- ~~修复`/playlist`加入歌单时，因为下载时间过长无法回复消息而报错的问题。~~
- 加入`/search`名字进行播放的功能。
- 现在能使用`/play`来播放歌单啦，然后把`/playlist`这个功能删除了~~【太呆了】~~。
- 现在能播放bilibili的视频音频啦。
- 进行了一个command指令输出的美化捏！现在的bot说话更好看了！
- **播放歌曲的时候，请将频道Bitrate限制在64kb及以下！**

---

# 当前音乐功能

| Command   | Description  |  Command   | Description  |
| -------   | -----------  | -------   | -----------  |
| `play`    | 暂停歌曲      |  `load Server` | 当bot离开时，保存当前未播放完成的歌单，并下次回来后输入`/load Server History` 即可播放之前未完成播放的歌单。 |
| `pause`   | 暂停歌曲      |   `load Mine` | 加载自己保存的歌单 |
| `skip`    | 跳过当前歌曲  |   `save [url]` | 保存链接中的歌单 |
| `skipto`  | 跳到指定歌曲  |   `report` | 报告错误给茶慕 |
| `skipall` | 跳过所有歌曲  |   `maze` | 获取茶慕的profile |
| `delete`  | 删除指定歌曲  |   `queue` | 显示当前歌单 |
| `current` | 显示当前歌曲  |   `current` | 显示当前歌曲 |
| `leave`   | 让bot离开频道 |   `search` | 搜索歌曲 |

# 当前聊天功能

| Command   | Description  |  Command   | Description  |
| -------   | -----------  | -------   | -----------  |
| `chatgpt_on`    | 开启聊天功能      |  `chatgpt_off` | 关闭聊天功能 |
| `set_chat_channel <channel>`   | 设置聊天频道      |   `set_music_channel <channel>` | 设置音乐频道 |
| `chatgpt_public_thread <name> <prompt>`    | 在Public Thread中聊天  |   `chatgpt_private_thread <name> <prompt>` | 在PrivateThread中聊天 |
| `delete_chat_channel <channel>`  | 删除该聊天频道的chatgpt功能  |   `delete_music_channel <channel>` | 删除该聊天频道的音乐口语指令功能 |
| `delete_current_thread`  | 删除当前Thread  | 

# 当前信息检索功能
| Command   | Description  |  Command   | Description  |
| -------   | -----------  | -------   | -----------  |
| `splatoon <mode>` | 查看splatoon3地图日历，在显示日历后可以点击按钮来查看接下来的地图。| `google <context>` | 在google上搜索内容 |
| `bilibili <context>` | 在bilibili上搜索内容 | `zhihu <context>` | 在知乎上搜索内容 |
| `ff14 <context>` | 在ff14灰机wiki上搜索内容 | `reddit <context>` | 在Reddit上搜索内容 |
| `stackoverflow <context>` | 在stackoverflow上搜索内容 | `bangumi <context>` | 在Bangumi上搜索内容 |
# 待改进的功能


- 还没想好捏


# 研发中


- [ ]  `Repeat` 重复当前歌曲
- [ ]  …

# 后续功能

- [ ]  支持Spotify
- [ ]  …


# 已知问题


- 无
