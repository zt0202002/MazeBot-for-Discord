from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from commands.music.cmd_join import join
from commands.music.cmd_queue import PAGE_SIZE
from commands.music.music_playlist import player
from pytube import Search
from bilibili_api import search as bilibili_search
import validators, asyncio



async def play(ctx, bot, input, msg=None):
    msg = await check_bot_in_channel(ctx, bot, msg=msg)
    if msg == None: # not_in_same_channel
        return

    # 搜索功能
    if not validators.url(input):
        msg = await search(ctx, bot, input, msg)
        return
    
    # 暂时不支持163
    if 'music.163.com' in input:
        await msg.edit(content='', embed=str_no_netease)
        return
    
    gid = ctx.guild.id
    print(f'添加列表: {input}')
    add_list_timer = datetime.now()
    num_of_new = await player.add_list(gid, input)
    print(f'列表耗时: {datetime.now()-add_list_timer}')
    if num_of_new <= 0: 
        await msg.edit(content='', embed=str_invalid_url)
        return

    await play_music(ctx, bot, msg, num_of_new)



async def check_bot_in_channel(ctx, bot, msg=None):
    if ctx.author.voice is None:
        if msg is None:
            msg = await ctx.send(embed=str_not_in_voice_channel)
        else:
            await msg.edit(content='', embed=str_not_in_voice_channel)
        return None
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    try:
        channel = ctx.author.voice.channel
    except:
        channel = ctx.message.channel
    
    if voice is None:
        msg = await join(ctx, bot, msg)
        
    elif voice.channel != channel:
        if msg is None:
            await ctx.send(embed=str_not_in_same_channel)
            return None
        else:
            await msg.edit(content='', embed=str_not_in_same_channel)
            return None

    # 现在bot在语音频道里，开始处理音频链接
    if msg is None:
        msg = await ctx.send(embed=str_loading_song)
    else:
        await msg.edit(content='', embed=str_loading_song)

    # 只有在发生错误时返回值是None
    return msg



async def play_music(ctx, bot, msg, num_of_new):
    voice = get(bot.voice_clients, guild=ctx.guild)
    gid = ctx.guild.id
    playlist = player.get_list(gid)
    is_edit_msg = False

    # 在往空列表加新歌时，播放第一首
    if num_of_new == len(playlist) and player.get_curr(gid) == {}:
        await player.play(ctx, bot)
        
        curr_info = player.get_curr(gid)
        if curr_info == {}:
            embed_var = str_invalid_url
            voice.stop()
            player.clear_playlist(gid)
        else:
            desc = f'{curr_info["title"]}\n{time_display(curr_info)}\n{curr_info["webpage_url"]}'
            embed_var = discord.Embed(title=f'我来播放这首歌了捏！', description=desc, color=SUCCESS)
            embed_var.set_image(url=curr_info['thumbnail'])
        if msg is None:
            await ctx.channel.send(embed=embed_var)
        else:
            await msg.edit(content='', embed=embed_var)
        is_edit_msg = True
    
    # 如果当前有歌曲播放，且如果只有一首新歌，显示playlist最后一首歌的名字和url
    elif num_of_new == 1:
        list_down_proc = asyncio.to_thread(player.download_list, gid)

        new_info = playlist[len(playlist)-1]
        desc = f'[{len(playlist)}]\t{new_info["title"]}\n{new_info["webpage_url"]}'
        embed_var = discord.Embed(title=f'我把这首歌加入播放列表了捏！', description=desc, color=SUCCESS)
        if msg is None:
            await ctx.channel.send(embed=embed_var)
        else:
            await msg.edit(content='', embed=embed_var)

        await list_down_proc

    # 如果新加入的歌不只一首，显示专辑中的歌的数量
    if num_of_new > 1:
        list_down_proc = asyncio.to_thread(player.download_list, gid)

        embed_var = discord.Embed(title=f'我把{num_of_new}首歌加入播放列表了捏！', color=SUCCESS)
        if is_edit_msg or msg is None:
            await ctx.channel.send(embed=embed_var)
        else:
            await msg.edit(content='', embed=embed_var)

        await list_down_proc



# async def search(ctx, bot, keywords, msg=None, search='BiliBili'):
async def search(ctx, bot, keywords, msg=None, search='youtube'):
    msg = await check_bot_in_channel(ctx, bot, msg=msg)
    if msg == None: # not_in_same_channel
        return

    # bilibili search
    if search == 'BiliBili':
        try:
            raw_results = await bilibili_search.search(keywords)
            # 20条结果
            search_results = list(filter(lambda item: item['result_type'] == "video", raw_results['result']))[0]['data']
            if search_results == []:
                await msg.edit(embed=str_no_search_result)   
            else: 
                queue_list_embed = bilibili_search_to_embed(search_results, 0)
                await msg.edit(content = '', embed=queue_list_embed, view=BiliBiliSearchButton(search_results=search_results))
        except Exception as e:
            print(e)
            await msg.edit(embed=str_no_search_result) 

    # youtube search
    elif search == 'youtube':
        try:
            search_results = Search(keywords).results
            if search_results == []:
                await msg.edit (embed=str_no_search_result)
            else:
                queue_list_embed = youtube_search_to_embed(search_results, 0)
                await msg.edit(content = '', embed=queue_list_embed, view=YouTubeSearchButton(search_results=search_results))
        except Exception as e:
            print(e)
            await msg.edit(embed=str_no_search_result) 



def youtube_search_to_embed(infos, start, end=PAGE_SIZE):
    embedVar = discord.Embed(title=f'我找到了这些歌！', description="", color=SUCCESS)
    if start + end > len(infos):
        end = len(infos)
    else:
        end += start
    for i in range(start, end):
        name = f'**[{i+1-start}] {infos[i].title[:37]}**'
        duration_str = timedelta(seconds=infos[i].length)
        value = f'{infos[i].author}\n[{duration_str}]\n{infos[i].watch_url}'
        embedVar.add_field(name=name, value=value, inline=False)
    return embedVar

class YouTubeSearchButton(discord.ui.View):
    def __init__(self, *, search_results, timeout=None):
        super().__init__(timeout=timeout)
        self.results = search_results
        self.index = 0

    @discord.ui.button(label="[1]", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, interaction, button):
        button.view.timeout = None
        if self.index <= len(self.results):
            await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)
            num_of_new = await player.add_list(interaction.guild.id, self.results[self.index].watch_url)
            await play_music(interaction, interaction.client, None, num_of_new)

    @discord.ui.button(label="[2]", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, interaction, button):
        button.view.timeout = None
        if self.index <= len(self.results):
            await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)
            num_of_new = await player.add_list(interaction.guild.id, self.results[self.index+1].watch_url)
            await play_music(interaction, interaction.client, None, num_of_new)

    @discord.ui.button(label="[3]", row=0, style=discord.ButtonStyle.primary)
    async def third_button_callback(self, interaction, button):
        button.view.timeout = None
        if self.index <= len(self.results):
            await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)
            num_of_new = await player.add_list(interaction.guild.id, self.results[self.index+2].watch_url)
            await play_music(interaction, interaction.client, None, num_of_new)

    @discord.ui.button(label="[4]", row=0, style=discord.ButtonStyle.primary)
    async def forth_button_callback(self, interaction, button):
        button.view.timeout = None
        if self.index <= len(self.results):
            await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)
            num_of_new = await player.add_list(interaction.guild.id, self.results[self.index+3].watch_url)
            await play_music(interaction, interaction.client, None, num_of_new)

    @discord.ui.button(label="[5]", row=0, style=discord.ButtonStyle.primary)
    async def fifth_button_callback(self, interaction, button):
        button.view.timeout = None
        if self.index <= len(self.results):
            await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)
            num_of_new = await player.add_list(interaction.guild.id, self.results[self.index+4].watch_url)
            await play_music(interaction, interaction.client, None, num_of_new)
    
    @discord.ui.button(label="前一页", row=1, style=discord.ButtonStyle.primary, disabled=False)
    async def prev_button_callback(self, interaction, button):
        button.view.timeout = None
        self.index = max(0, self.index - PAGE_SIZE)
        embed_var = youtube_search_to_embed(self.results, self.index)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)

    @discord.ui.button(label="后一页", row=1, style=discord.ButtonStyle.primary, disabled=False)
    async def next_button_callback(self, interaction, button):
        button.view.timeout = None
        remainder = (len(self.results)-1) % PAGE_SIZE + 1 # 当len能被整除时余一页
        if self.index + PAGE_SIZE >= len(self.results):
            self.index = len(self.results) - remainder
        else:
            self.index+= PAGE_SIZE
        embed_var = youtube_search_to_embed(self.results, self.index)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)
    
    @discord.ui.button(label="关闭菜单", row=1, style=discord.ButtonStyle.danger)
    async def delete_button_callback(self, interaction, button):
        button.view.timeout = None
        await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)



def bilibili_search_to_embed(infos, start, end=PAGE_SIZE):
    embedVar = discord.Embed(title=f'我找到了这些歌！', description="", color=SUCCESS)
    if start + end >= len(infos):
        end = len(infos)
    else:
        end += start
    for i in range(start, end):
        title = infos[i]['title'].replace('<em class="keyword">', '').replace('</em>', '')
        name = f'**[{i+1-start}] {title[:37]}**'
        value = f'{infos[i]["author"]}\n[{infos[i]["duration"]}]\nhttp://www.bilibili.com/video/{infos[i]["bvid"]}'
        embedVar.add_field(name=name, value=value, inline=False)
    return embedVar

class BiliBiliSearchButton(discord.ui.View):
    def __init__(self, *, search_results, timeout=None):
        super().__init__(timeout=timeout)
        self.results = search_results
        self.index = 0

    @discord.ui.button(label="[1]", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, interaction, button):
        button.view.timeout = None
        if self.index <= len(self.results):
            await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)
            url = f'http://www.bilibili.com/video/{self.results[self.index]["bvid"]}'
            num_of_new = await player.add_list(interaction.guild.id, url)
            await play_music(interaction, interaction.client, None, num_of_new)
            

    @discord.ui.button(label="[2]", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, interaction, button):
        button.view.timeout = None
        if self.index + 1 <= len(self.results):
            await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)
            url = f'http://www.bilibili.com/video/{self.results[self.index+1]["bvid"]}'
            num_of_new = await player.add_list(interaction.guild.id, url)
            await play_music(interaction, interaction.client, None, num_of_new)

    @discord.ui.button(label="[3]", row=0, style=discord.ButtonStyle.primary)
    async def third_button_callback(self, interaction, button):
        button.view.timeout = None
        if self.index + 2 <= len(self.results):
            await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)
            url = f'http://www.bilibili.com/video/{self.results[self.index+2]["bvid"]}'
            num_of_new = await player.add_list(interaction.guild.id, url)
            await play_music(interaction, interaction.client, None, num_of_new)

    @discord.ui.button(label="[4]", row=0, style=discord.ButtonStyle.primary)
    async def forth_button_callback(self, interaction, button):
        button.view.timeout = None
        if self.index + 3 <= len(self.results):
            await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)
            url = f'http://www.bilibili.com/video/{self.results[self.index+3]["bvid"]}'
            num_of_new = await player.add_list(interaction.guild.id, url)
            await play_music(interaction, interaction.client, None, num_of_new)

    @discord.ui.button(label="[5]", row=0, style=discord.ButtonStyle.primary)
    async def fifth_button_callback(self, interaction, button):
        button.view.timeout = None
        if self.index + 4 <= len(self.results):
            await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)
            url = f'http://www.bilibili.com/video/{self.results[self.index+4]["bvid"]}'
            num_of_new = await player.add_list(interaction.guild.id, url)
            await play_music(interaction, interaction.client, None, num_of_new)
            await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)
    
    @discord.ui.button(label="前一页", row=1, style=discord.ButtonStyle.primary, disabled=False)
    async def prev_button_callback(self, interaction, button):
        button.view.timeout = None
        self.index = max(0, self.index - PAGE_SIZE)
        embed_var = bilibili_search_to_embed(self.results, self.index)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)

    @discord.ui.button(label="后一页", row=1, style=discord.ButtonStyle.primary, disabled=False)
    async def next_button_callback(self, interaction, button):
        button.view.timeout = None
        remainder = (len(self.results)-1) % PAGE_SIZE + 1 # 当len能被整除时余一页
        if self.index + PAGE_SIZE >= len(self.results): 
            self.index = len(self.results) - remainder
        else:
            self.index+= PAGE_SIZE
        embed_var = bilibili_search_to_embed(self.results, self.index)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)
    
    @discord.ui.button(label="关闭菜单", row=1, style=discord.ButtonStyle.danger)
    async def delete_button_callback(self, interaction, button):
        button.view.timeout = None
        await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)