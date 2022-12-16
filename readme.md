# 马子的MazeBot for Discord
---

> **这里是马子的音乐bot，后续内容更新中…**
> 

> **目前马子的音乐bot会随机回复一些话（功能无法关闭）**
> 

---
### Related Links:
- **[MazeBot for Discord App](https://discord.com/api/oauth2/authorize?client_id=1051385856134488124&permissions=1643315723888&scope=applications.commands%20bot)**
- **[马子茶慕的Notion](https://www.notion.so/Notion-14b0d5588f804acbb39ce58bc37e978e)** 

# Update Note

---

### December 16, 2022

- 规划整理了下当前的代码文件，将各个function写入单独的python文件中。
- 当bot所在频道没人的时候，bot会自动离开。
- 当bot离开时，保存当前未完成播放的歌单，并下次回来后输入`/loading Server History` 即可播放之前未完成播放的歌单。

### December 14, 2022

- 现在输入`/current` 和`/queue` 能够显示当前歌曲播放的时间了!
- 现在输入`/leave` 指令能够让bot离开语音频道了！
- 现在输入`/maze` 指令能够获取马子的profile了！
- 现在输入`/report` 指令能够报告错误给马子了！

### December 13, 2022

- ~~修复`/playlist`加入歌单时，因为下载时间过长无法回复消息而报错的问题。~~
- 加入`/search`名字进行播放的功能。
- 现在能使用`/play`来播放歌单啦，然后把`/playlist`这个功能删除了~~【太呆了】~~。
- 现在能播放bilibili的视频音频啦。
- 进行了一个command指令输出的美化捏！现在的bot说话更好看了！
- **播放歌曲的时候，请将频道Bitrate限制在64kb及以下！**

---

# 当前功能

---

- [x]  `Play`
    - [x]  播放Bilibili, Youtube
- [x]  `Pause`
- [x]  `Skip`
- [x]  `Skipto`
- [x]  `Delete`
- [x]  `Current`
- [x]  `Leave`
    - [x]  当频道空无一人时，bot自动离开频道
- [x]  `loading Server History`当bot离开时，保存当前未播放完成的歌单，并下次回来后继续播放

# 待改进的功能

---

- [ ]  `Search`
    - [x]  search 名字
    - [ ]  显示可选列表
    - [ ]  让client选择一首播放
- [ ]  `Queue`
    - [x]  显示当前歌曲列表
    - [x]  美化列表
    - [ ]  选择歌曲进行切歌
    - [ ]  分页

---

# 研发中

---

- [ ]  skipall
- [ ]  …

# 后续功能

---

- [ ]  `Repeat` 重复当前歌曲
- [ ]  ChatGPT
- [ ]  保存未播放完成的歌单
- [ ]  创建自己的歌单
- [ ]  支持Spotify
- [ ]  …

---

# 已知问题

---

- [ ]  `/pause` 时，无法读取当前列表中的歌，会显示当前🈚️歌曲播放。
- [ ]  …