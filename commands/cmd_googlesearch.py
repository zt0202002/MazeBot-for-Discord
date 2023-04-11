from googleapiclient.discovery import build
import os
import discord
from bs4 import BeautifulSoup
from urllib.request import urlopen

async def google_search_func(query, cx, type, num_results=3):
    api_key = os.getenv('GOOGLE_SEARCH_API')

    service = build("customsearch", "v1", developerKey=api_key)
    response = service.cse().list(q=query, cx=cx, num=num_results).execute()

    embedVar = discord.Embed(title=f'{type} Search Results for {query}', description='', color=0x8B4C39)

    for i, item in enumerate(response['items']):
        embedVar.add_field(name=f"**{i+1}. {item['title']}**", value=f"{item['snippet']}\n{item['link']}", inline=False)

    return embedVar

async def google(ctx, query):
    cx = os.getenv('CX_GOOGLE')
    embedVar = await google_search_func(query, cx, 'Google')
    await ctx.reply(embed=embedVar)

async def reddit(ctx, query):
    cx = os.getenv('CX_REDDIT')
    embedVar = await google_search_func(query, cx, 'Reddit')
    await ctx.reply(embed=embedVar)

async def stackoverflow(ctx, query):
    cx = os.getenv('CX_STACKOVERFLOW')
    embedVar = await google_search_func(query, cx, 'Stackoverflow')
    await ctx.reply(embed=embedVar)

async def bilibili(ctx, query):
    cx = os.getenv('CX_BILIBILI')
    embedVar = await google_search_func(query, cx, 'Bilibili')
    await ctx.reply(embed=embedVar)

async def moe(ctx, query):
    cx = os.getenv('CX_MOE')
    embedVar = await google_search_func(query, cx, '萌娘百科')
    await ctx.reply(embed=embedVar)

async def ffxiv(ctx, query):
    cx = os.getenv('CX_FFXIV')
    embedVar = await google_search_func(query, cx, 'Huiji FF14 Wiki')
    await ctx.reply(embed=embedVar)

async def news(ctx):
    try:
        await ctx.interaction.response.defer(thinking=True)
        link = 'https://world.huanqiu.com/'
        url = urlopen(link).read()

        soup = BeautifulSoup(url.decode('utf-8'), 'lxml')
        today_important_news = soup.find_all(class_='csr_sketch_txt_3')

        news = today_important_news[0].find_all('div')
        
        embedVar = discord.Embed(title=f'今日要闻', description='', color=0x8B4C39)

        for new in news[2:]:
            title = new.find_all('textarea')[2]
            link = 'https://world.huanqiu.com/article/' + new.find_all('textarea')[0].get_text()
            embedVar.add_field(name=f"**{title.get_text()}**", value=f"{link}", inline=False)

        today_recommand_news = soup.find_all(class_='csr_image_img_6_subtitle')
        news = today_recommand_news[0].find_all('div')
        for new in news[2:]:
            title = new.find_all('textarea')[3]
            link = 'https://world.huanqiu.com/article/' + new.find_all('textarea')[0].get_text()
            embedVar.add_field(name=f"**{title.get_text()}**", value=f"{link}", inline=False)
        
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

        length = 0

        for new in news:
            title = new.find('a').find('div').get('title')
            link = 'https://www.yystv.cn' + new.find('a').get('href')

            embedVar.add_field(name=f"**{title}**", value=f"{link}", inline=False)

            # if length == 5: break
            length += 1
        
        await ctx.reply(embed=embedVar)

    except Exception:
        await ctx.reply('游戏新闻获取失败')