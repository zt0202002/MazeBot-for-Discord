from discord.utils import get
from help_functions.help_text import *
from help_functions.help_time import *
from help_functions.help_queue import *

async def queue(ctx, bot):
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    cur = str_loading_song
    cur.color = 0x487B60
    msg = await ctx.send(embed=cur)


    if ctx.guild.id not in current_song or current_song[ctx.guild.id] == {}:
        await msg.edit(content = '', embed=str_not_song_playing)
    else:
        current = current_song[ctx.guild.id]['info']

        timer = check_time(current_song[ctx.guild.id])

        if ctx.guild.id not in song_queue or len(song_queue[ctx.guild.id]) == 0:
            embedVar = discord.Embed(title=f'当前播放:\n[1] {current["title"]} [{timer[0]}/{timer[1]}]\n', description=f'', color=0x487B60)
            await msg.edit(content = '', embed=embedVar)
        else:
            queue = song_queue[ctx.guild.id]
            queue_list = ''
            for i in range(len(queue)):
                queue_list += f'[{i+2}]\t {queue[i].title}\n'
            embedVar = discord.Embed(title=f'当前播放:\n[1] {current["title"]} [{timer[0]}/{timer[1]}]\n', description=f'{queue_list}', color=0x487B60)
            await msg.edit(content = '', embed=embedVar)