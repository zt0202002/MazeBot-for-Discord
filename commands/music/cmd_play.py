from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from commands.music.cmd_join import join
from commands.music.music_playlist import player
from commands.music.cmd_resume import resume
# from commands.music.cmd_search import search
from pytube import Search
from bilibili_api import search as bilibili_search
from commands.music.cmd_queue import PAGE_SIZE

import validators



async def play(ctx, bot, input, msg=None):
    if input is None: await resume(ctx, bot); return

    voice = get(bot.voice_clients, guild=ctx.guild)
    try:    channel = ctx.author.voice.channel
    except: channel = ctx.message.channel

    if voice is None:
        msg = await join(ctx, bot)
        
    elif voice.channel != channel:
        if msg is None: await ctx.send(embed=str_not_in_same_channel); return
        else:           await msg.edit(content='', embed=str_not_in_same_channel); return

    # 会拒绝没有http或者https的链接
    if not validators.url(input): await search(ctx, bot, input, msg); return

    # 现在bot在语音频道里，开始处理音频链接
    if msg is None: msg = await ctx.send(embed=str_loading_song)
    else:                 await msg.edit(content='', embed=str_loading_song)
    
    gid = ctx.guild.id
    num_of_new = await player.add_list(gid, input)
    if num_of_new <= 0: await msg.edit(content='', embed=str_invalid_url); return

    await play_music(ctx, bot, msg, num_of_new)
    

async def play_music(ctx, bot, msg, num_of_new):
    voice = get(bot.voice_clients, guild=ctx.guild)
    gid = ctx.guild.id
    playlist = player.get_list(gid)
    is_edit_msg = False

    # 往空列表加新歌，播放第一首
    if num_of_new == len(playlist) and not voice.is_playing():
        player.play(ctx)
        curr_info = player.get_curr(gid)
        desc = f'{curr_info["title"]}\n{time_display(curr_info)}\n{curr_info["webpage_url"]}'
        embed_var = discord.Embed(title=f'我来播放这首歌了捏！', description=desc, color=SUCCESS)
        if msg is None: await ctx.channel.send(embed=embed_var)
        else:           await msg.edit(content='', embed=embed_var)
        is_edit_msg = True
    
    # 如果当前有歌曲播放，且如果只有一首新歌，print出来playlist最后一首歌的名字和url
    elif num_of_new == 1:
        new_info = playlist[ctx.guild.id][-1]
        desc = f'[{len(playlist)+1}]\t{new_info["title"]}\n{new_info["webpage_url"]}'
        embed_var = discord.Embed(title=f'我把这首歌加入播放列表了捏！', description=desc, color=SUCCESS)
        if msg is None: await ctx.channel.send(embed=embed_var)
        else:           await msg.edit(content='', embed=embed_var)

    # 如果新加入的歌不只一首，print出来专辑中的歌的数量
    if num_of_new > 1:
        embed_var = discord.Embed(title=f'我把{num_of_new}首歌加入播放列表了捏！', color=SUCCESS)
        if is_edit_msg or msg is None: await ctx.channel.send(embed=embed_var)
        else:                          await msg.edit(content='', embed=embed_var)


async def search(ctx, bot, keywords, msg=None):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if msg is not None: channel = ctx.author.voice.channel
    else:               channel = ctx.message.author.voice.channel

    if voice is None:
        msg = await join(ctx, bot, msg)
    elif voice.channel != channel:      
        embedVar = str_not_in_same_channel
        if msg is None: await ctx.send(embed=embedVar)
        else:           await msg.edit(content='', embed=embedVar) 

    if msg is None: msg = await ctx.send(embed=str_loading_song)

    # bilibili search
    try:
        raw_results = await bilibili_search.search(keywords)
        search_results = list(filter(lambda item: item['result_type'] == "video", raw_results['result']))[0]['data']
        if search_results == []:
            await msg.edit(embed=str_no_search_result)   
        else: 
            queue_list_embed = bilibili_search_to_embed(search_results, 0)        
            await msg.edit(content = '', embed=queue_list_embed, view=BiliBiliSearchButton(search_results=search_results))
    except:
        await msg.edit(embed=str_no_search_result) 

    # # youtube search
    # try:
    #     search_results = Search(keywords).results
    #     if search_results == []:
    #         await msg.edit (embed=str_no_search_result)   
    #     else: 
    #         queue_list_embed = youtube_search_to_embed(search_results, 0)        
    #         await msg.edit(content = '', embed=queue_list_embed, view=YouTubeSearchButton(search_results=search_results))
    # except:
    #     await msg.edit(embed=str_no_search_result) 



# def youtube_search_to_embed(infos, start, end=PAGE_SIZE):
#     embedVar = discord.Embed(title=f'我找到了这些歌！', description="", color=SUCCESS)
#     if start + end > len(infos): end = len(infos)
#     else: end += start
#     for i in range(start, end):
#         embedVar.add_field(name=f'**[{i+1-start}] {infos[i].title}**', value=f'{infos[i].watch_url}', inline=False)
#     return embedVar



# class YouTubeSearchButton(discord.ui.View):
    # def __init__(self, *, search_results, timeout=None):
    #     super().__init__(timeout=timeout)
    #     self.results = search_results

    # @discord.ui.button(label="1", row=0, style=discord.ButtonStyle.primary)
    # async def first_button_callback(self, interaction, button):
    #     button.view.timeout = None
    #     num_of_new = await player.add_list(interaction.guild.id, self.results[0].watch_url)
    #     await play_music(interaction, interaction.client, None, num_of_new)
    #     await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)

    # @discord.ui.button(label="2", row=0, style=discord.ButtonStyle.primary)
    # async def second_button_callback(self, interaction, button):
    #     button.view.timeout = None
    #     num_of_new = await player.add_list(interaction.guild.id, self.results[1].watch_url)
    #     await play_music(interaction, interaction.client, None, num_of_new)
    #     await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)

    # @discord.ui.button(label="3", row=0, style=discord.ButtonStyle.primary)
    # async def third_button_callback(self, interaction, button):
    #     button.view.timeout = None
    #     num_of_new = await player.add_list(interaction.guild.id, self.results[2].watch_url)
    #     await play_music(interaction, interaction.client, None, num_of_new)
    #     await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)

    # @discord.ui.button(label="4", row=0, style=discord.ButtonStyle.primary)
    # async def forth_button_callback(self, interaction, button):
    #     button.view.timeout = None
    #     num_of_new = await player.add_list(interaction.guild.id, self.results[3].watch_url)
    #     await play_music(interaction, interaction.client, None, num_of_new)
    #     await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)

    # @discord.ui.button(label="5", row=0, style=discord.ButtonStyle.primary)
    # async def fifth_button_callback(self, interaction, button):
    #     button.view.timeout = None
    #     num_of_new = await player.add_list(interaction.guild.id, self.results[4].watch_url)
    #     await play_music(interaction, interaction.client, None, num_of_new)
    #     await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)

    # @discord.ui.button(label="X", row=0, style=discord.ButtonStyle.danger)
    # async def delete_button_callback(self, interaction, button):
    #     button.view.timeout = None
    #     await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)



def bilibili_search_to_embed(infos, start, end=PAGE_SIZE):
    embedVar = discord.Embed(title=f'我找到了这些歌！', description="", color=SUCCESS)
    if start + end > len(infos): end = len(infos)
    else: end += start
    for i in range(start, end):
        url = f'http://www.bilibili.com/video/{infos[i]["bvid"]}'
        title = infos[i]['title'].replace('<em class="keyword">', '').replace('</em>', '')
        embedVar.add_field(name=f'**[{i+1-start}] {title[:38]}**', value=url, inline=False)
    return embedVar


class BiliBiliSearchButton(discord.ui.View):
    def __init__(self, *, search_results, timeout=None):
        super().__init__(timeout=timeout)
        self.results = search_results

    @discord.ui.button(label="1", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, interaction, button):
        button.view.timeout = None
        url = f'http://www.bilibili.com/video/{self.results[0]["bvid"]}'
        num_of_new = await player.add_list(interaction.guild.id, url)
        await play_music(interaction, interaction.client, None, num_of_new)
        await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)

    @discord.ui.button(label="2", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, interaction, button):
        button.view.timeout = None
        url = f'http://www.bilibili.com/video/{self.results[1]["bvid"]}'
        num_of_new = await player.add_list(interaction.guild.id, url)
        await play_music(interaction, interaction.client, None, num_of_new)
        await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)

    @discord.ui.button(label="3", row=0, style=discord.ButtonStyle.primary)
    async def third_button_callback(self, interaction, button):
        button.view.timeout = None
        url = f'http://www.bilibili.com/video/{self.results[2]["bvid"]}'
        num_of_new = await player.add_list(interaction.guild.id, url)
        await play_music(interaction, interaction.client, None, num_of_new)
        await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)

    @discord.ui.button(label="4", row=0, style=discord.ButtonStyle.primary)
    async def forth_button_callback(self, interaction, button):
        button.view.timeout = None
        url = f'http://www.bilibili.com/video/{self.results[3]["bvid"]}'
        num_of_new = await player.add_list(interaction.guild.id, url)
        await play_music(interaction, interaction.client, None, num_of_new)
        await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)

    @discord.ui.button(label="5", row=0, style=discord.ButtonStyle.primary)
    async def fifth_button_callback(self, interaction, button):
        button.view.timeout = None
        url = f'http://www.bilibili.com/video/{self.results[4]["bvid"]}'
        num_of_new = await player.add_list(interaction.guild.id, url)
        await play_music(interaction, interaction.client, None, num_of_new)
        await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)

    @discord.ui.button(label="X", row=1, style=discord.ButtonStyle.danger)
    async def delete_button_callback(self, interaction, button):
        button.view.timeout = None
        await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)