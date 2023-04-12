from googleapiclient.discovery import build
import os
import discord
from bs4 import BeautifulSoup
from urllib.request import urlopen

GOOGLE_SEARCH_INDEX = {}

class GoogleSearchButton(discord.ui.View):
    global GOOGLE_SEARCH_INDEX

    def get_msg(self, interaction):
        gid = interaction.message.id
        index, queue = GOOGLE_SEARCH_INDEX[gid]['index'], GOOGLE_SEARCH_INDEX[gid]['queue']
        type, query = GOOGLE_SEARCH_INDEX[gid]['type'], GOOGLE_SEARCH_INDEX[gid]['query']
        return gid, index, queue, type, query
    
    @discord.ui.button(label="Prev", row=0, style=discord.ButtonStyle.primary)
    async def prev_button_callback(self, interaction, button):
        gid, index, queue, type, query = self.get_msg(interaction)
        if index - 3 < 0:   index = 0
        else:   index -= 3

        GOOGLE_SEARCH_INDEX[gid]['index'] = index

        embedVar, a, b = await search_result_embed(query, queue, type, index)
        await interaction.response.edit_message(content = '', embed=embedVar, view=self)
    
    @discord.ui.button(label="Next", row=0, style=discord.ButtonStyle.primary)
    async def next_button_callback(self, interaction, button):
        gid, index, queue, type, query = self.get_msg(interaction)
        if index + 3 >= len(queue):     index = len(queue) - 3
        else:                           index += 3

        if index < 0:   index = 0

        GOOGLE_SEARCH_INDEX[gid]['index'] = index

        embedVar, a, b = await search_result_embed(query, queue, type, index)
        await interaction.response.edit_message(content = '', embed=embedVar, view=self)


async def search_result_embed(query, results, type, index):
    embedVar = discord.Embed(title=f'{type} Search Results for {query}', description='', color=0x8B4C39)

    for i, item in enumerate(results):
        if i < index:   continue
        if i >= index + 3:  break
        embedVar.add_field(name=f"**{i+1}. {item['title']}**", value=f"{item['snippet']}\n{item['link']}", inline=False)

    return embedVar, index, results

async def google_search_func(query, cx, type, num_results=9, index=0):
    api_key = os.getenv('GOOGLE_SEARCH_API')

    service = build("customsearch", "v1", developerKey=api_key)
    response = service.cse().list(q=query, cx=cx, num=num_results).execute()

    results = response['items']

    return await search_result_embed(query, results, type, index)

async def reply_google_search(ctx, query, type, embedVar, index, results):
    global GOOGLE_SEARCH_INDEX

    msg = await ctx.reply(embed=embedVar, view=GoogleSearchButton())
    GOOGLE_SEARCH_INDEX[msg.id] = {'index': index, 'queue': results, 'type': type, 'query': query}

async def google(ctx, query):
    cx = os.getenv('CX_GOOGLE')
    embedVar, index, results = await google_search_func(query, cx, 'Google')
    await reply_google_search(ctx, query, 'Google', embedVar, index, results)
    
async def reddit(ctx, query):
    cx = os.getenv('CX_REDDIT')
    embedVar, index, results = await google_search_func(query, cx, 'Reddit')
    await reply_google_search(ctx, query, 'Reddit', embedVar, index, results)

async def stackoverflow(ctx, query):
    cx = os.getenv('CX_STACKOVERFLOW')
    embedVar, index, results = await google_search_func(query, cx, 'StackOverflow')
    await reply_google_search(ctx, query, 'StackOverflow', embedVar, index, results)

async def bilibili(ctx, query):
    cx = os.getenv('CX_BILIBILI')
    embedVar, index, results = await google_search_func(query, cx, 'Bilibili')
    await reply_google_search(ctx, query, 'Bilibili', embedVar, index, results)

async def moe(ctx, query):
    cx = os.getenv('CX_MOE')
    embedVar, index, results = await google_search_func(query, cx, '萌娘百科')
    await reply_google_search(ctx, query, '萌娘百科', embedVar, index, results)
    
async def ffxiv(ctx, query):
    cx = os.getenv('CX_FFXIV')
    embedVar, index, results = await google_search_func(query, cx, 'FFXIV')
    await reply_google_search(ctx, query, 'FFXIV', embedVar, index, results)

async def zhihu(ctx, query):
    cx = os.getenv('CX_ZHIHU')
    embedVar, index, results = await google_search_func(query, cx, '知乎')
    await reply_google_search(ctx, query, '知乎', embedVar, index, results)

async def bangumi(ctx, query):
    cx = os.getenv('CX_BANGUMI')
    embedVar, index, results = await google_search_func(query, cx, 'Bangumi')
    await reply_google_search(ctx, query, 'Bangumi', embedVar, index, results)

async def news(ctx):
    try:
        await ctx.interaction.response.defer(thinking=True)
        link = 'https://world.huanqiu.com/'
        url = urlopen(link).read()

        soup = BeautifulSoup(url.decode('utf-8'), 'lxml')
        today_important_news = soup.find_all(class_='csr_sketch_txt_3')

        news = today_important_news[0].find_all('div')
        
        embedVar = discord.Embed(title=f'今日要闻', description='', color=0x8B4C39)

        i = 0

        for new in news[2:]:
            title = new.find_all('textarea')[2]
            link = 'https://world.huanqiu.com/article/' + new.find_all('textarea')[0].get_text()
            embedVar.add_field(name=f"**{i+1}. {title.get_text()}**", value=f"{link}", inline=False)
            i += 1

        today_recommand_news = soup.find_all(class_='csr_image_img_6_subtitle')
        news = today_recommand_news[0].find_all('div')
        for new in news[2:]:
            title = new.find_all('textarea')[3]
            link = 'https://world.huanqiu.com/article/' + new.find_all('textarea')[0].get_text()
            embedVar.add_field(name=f"**{i+1}. {title.get_text()}**", value=f"{link}", inline=False)
            i += 1
        
        await ctx.reply(embed=embedVar)
    except Exception:
        await ctx.reply('今日要闻获取失败')

async def game_news(ctx):
    try:
        await ctx.interaction.response.defer(thinking=True)
        link = 'https://www.yystv.cn/docs'
        url = urlopen(link).read()
        soup = BeautifulSoup(url.decode('utf-8'), 'lxml')
        news = soup.find_all(class_='list-container')[0].find_all('li')

        embedVar = discord.Embed(title=f'游戏新闻', description='', color=0x8B4C39)

        i = 0
        for new in news:
            title = new.find('a').find('div').get('title')
            link = 'https://www.yystv.cn' + new.find('a').get('href')

            embedVar.add_field(name=f"**{i+1}. {title}**", value=f"{link}", inline=False)

            i+=1
        
        await ctx.reply(embed=embedVar)

    except Exception:
        await ctx.reply('游戏新闻获取失败')