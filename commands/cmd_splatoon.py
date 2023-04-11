import discord
import requests
import pytz
from datetime import datetime

SPLATOON_INDEX={}

class SplatoonButton(discord.ui.View):
    global SPLATOON_INDEX

    def get_msg(self, interaction):
        mid = interaction.message.id
        index = SPLATOON_INDEX[mid]['index']
        mode = SPLATOON_INDEX[mid]['mode']
        return mid, index, mode

    @discord.ui.button(label="Prev", row=0, style=discord.ButtonStyle.primary)
    async def prev_button_callback(self, interaction, button):
        mid, index, mode = self.get_msg(interaction)
        if index - 1 < 0: index = 0
        else: index -= 1
        
        embeds = await get_splatoon_info(mode, index)
        SPLATOON_INDEX[mid]['index'] = index

        await interaction.response.edit_message(content = '', embeds=embeds, view=self)
    
    @discord.ui.button(label="Next", row=0, style=discord.ButtonStyle.primary)
    async def next_button_callback(self, interaction, button):
        mid, index, mode = self.get_msg(interaction)
        if mode == 'big run' or mode == 'pve team':
            embeds = await get_splatoon_info(mode, index)
            await interaction.response.edit_message(content = '', embeds=embeds, view=self)
        else:
            if index + 1 >= 10: index = 9
            else: index += 1
            embeds = await get_splatoon_info(mode, index)
            SPLATOON_INDEX[mid]['index'] = index

            await interaction.response.edit_message(content = '', embeds=embeds, view=self)

        
def read_schedule(type, index = 0):
    def read_regular(regular, index=0):
        startTime = regular[index]['startTime']
        endTime = regular[index]['endTime']
        vsStage_1 = regular[index]['regularMatchSetting']['vsStages'][0]
        vsStage_2 = regular[index]['regularMatchSetting']['vsStages'][1]
        mode = regular[index]['regularMatchSetting']['vsRule']['name']

        return {'startTime': startTime, 'endTime': endTime, 'vsStage': [vsStage_1, vsStage_2], 'mode': mode}

    def read_rank(rank, index=0):
        startTime = rank[index]['startTime']
        endTime = rank[index]['endTime']
        vsStage_1 = rank[index]['bankaraMatchSettings'][0]['vsStages'][0]
        vsStage_2 = rank[index]['bankaraMatchSettings'][0]['vsStages'][1]
        mode = rank[index]['bankaraMatchSettings'][0]['vsRule']['name']

        # print(startTime, endTime, vsStage_1['name'], vsStage_2['name'], mode)
        return {'startTime': startTime, 'endTime': endTime, 'vsStage': [vsStage_1, vsStage_2], 'mode': mode}

    def read_open_rank(rank, index=0):
        startTime = rank[index]['startTime']
        endTime = rank[index]['endTime']
        vsStage_1 = rank[index]['bankaraMatchSettings'][1]['vsStages'][0]
        vsStage_2 = rank[index]['bankaraMatchSettings'][1]['vsStages'][1]
        mode = rank[index]['bankaraMatchSettings'][1]['vsRule']['name']

        # print(startTime, endTime, vsStage_1['name'], vsStage_2['name'], mode)
        return {'startTime': startTime, 'endTime': endTime, 'vsStage': [vsStage_1, vsStage_2], 'mode': mode}

    def read_x_rank(rank, index=0):
        startTime = rank[index]['startTime']
        endTime = rank[index]['endTime']
        vsStage_1 = rank[index]['xMatchSetting']['vsStages'][0]
        vsStage_2 = rank[index]['xMatchSetting']['vsStages'][1]
        mode = rank[index]['xMatchSetting']['vsRule']['name']

        return {'startTime': startTime, 'endTime': endTime, 'vsStage': [vsStage_1, vsStage_2], 'mode': mode}

    def read_pve_regular(regular, index=0):
        startTime = regular[index]['startTime']
        endTime = regular[index]['endTime']
        coopStage = regular[index]['setting']['coopStage']
        weapons = regular[index]['setting']['weapons'] 

        return {'startTime': startTime, 'endTime': endTime, 'coopStage': coopStage, 'weapons': weapons}

    def read_pve_big_run(regular, index=0):
        if len(regular) == 0:
            return None
        else:
            return 'Working...'
        
    def read_pve_team(regular, index=0):
        if len(regular) == 0:
            return None
        startTime = regular[index]['startTime']
        endTime = regular[index]['endTime']
        coopStage = regular[index]['setting']['coopStage']
        weapons = regular[index]['setting']['weapons']

        return {'startTime': startTime, 'endTime': endTime, 'coopStage': coopStage, 'weapons': weapons}

    def get_result(type, index=0):
        link = 'https://splatoon3.ink/data/schedules.json'
        response = requests.get(link)
        schedule = dict(response.json())['data']

        # schecdule
        if type == 'regular':
            regular     = schedule['regularSchedules']['nodes']
            return read_regular(regular, index)
        elif type == 'rank':
            rank        = schedule['bankaraSchedules']['nodes']
            return read_rank(rank, index)
        elif type == 'open_rank':
            rank        = schedule['bankaraSchedules']['nodes']
            return read_open_rank(rank, index)
        elif type == 'x_rank':
            x_rank      = schedule['xSchedules']['nodes']
            return read_x_rank(x_rank, index)
        elif type == 'pve':
            pveRegular  = schedule['coopGroupingSchedule']['regularSchedules']['nodes']
            return read_pve_regular(pveRegular, index)
        elif type == 'big run':
            pveBigRun   = schedule['coopGroupingSchedule']['bigRunSchedules']['nodes']
            return read_pve_big_run(pveBigRun, index)
        elif type == 'pve team':
            pveTeam     = schedule['coopGroupingSchedule']['teamContestSchedules']['nodes']
            return read_pve_team(pveTeam, index)
    
    return get_result(type, index)

async def get_splatoon_info(type, index=0):
    global SPLATOON_INDEX
    result = read_schedule(type, index)
    
    status = 'Current'

    if index == 0:      status = 'Current'
    elif index == 1:    status = 'Next'
    elif index == 2:    status = '2nd Next'
    elif index == 3:    status = '3rd Next'
    else:               status = f'{index}th Next'

    
    if result != None: 
        timeZone = pytz.timezone('America/New_York')
    
        startTime = result['startTime']
        startTime = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc).astimezone(timeZone).strftime('%Y-%m-%d %H:%M:%S')
        endTime = result['endTime']
        endTime = datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc).astimezone(timeZone).strftime('%Y-%m-%d %H:%M:%S')
        
        desc = f'{startTime} ~ {endTime}'

    if type == 'regular': embed = discord.Embed(title=f'{status} Turf War | {result["mode"]}', description=desc, color=0x8B4C39)
    elif type == 'rank': embed = discord.Embed(title=f'{status} Ranked Battle | {result["mode"]}', description=desc, color=0x8B4C39)
    elif type == 'open_rank': embed = discord.Embed(title=f'{status} Open Ranked Battle | {result["mode"]}', description=desc, color=0x8B4C39)
    elif type == 'x_rank': embed = discord.Embed(title=f'{status} X Ranked Battle | {result["mode"]}', description=desc, color=0x8B4C39)
    elif type == 'pve': embed = discord.Embed(title=f'{status} PVE | {result["coopStage"]["name"]}', description=desc, color=0x8B4C39)
    elif type == 'big run': 
        if result == None:  embed = discord.Embed(title=f'{status} Big Run | None', description=f'', color=0x8B4C39)
        else:               embed = discord.Embed(title=f'{status} Big Run | {result["coopStage"]["name"]}', description=desc, color=0x8B4C39)
    elif type == 'pve team': 
        if result == None:  embed = discord.Embed(title=f'{status} Team PVE | None', description=f'', color=0x8B4C39)
        else:               embed = discord.Embed(title=f'{status} Team PVE | {result["coopStage"]["name"]}', description=desc, color=0x8B4C39)

    embed.set_thumbnail(url='https://fedi.splatoon3.ink/media/9da32c20-8159-4f0d-bcda-6bae9f582545/Splatoon3%20Twitter%20avatar.png')

    if result == None:  return [embed]

    if 'pve' not in type:
        embed1 = discord.Embed(title=f'**{result["vsStage"][0]["name"]}**', description=f'', color=0x8B4C39)
        embed2 = discord.Embed(title=f'**{result["vsStage"][1]["name"]}**', description=f'', color=0x8B4C39)
        embed1.set_image(url = result['vsStage'][0]['image']['url'])
        embed2.set_image(url = result['vsStage'][1]['image']['url'])

        embeds = [embed, embed1, embed2]
    else:
        embed.set_image(url = result['coopStage']['image']['url'])
        embed1 = discord.Embed(title=f"**{result['weapons'][0]['name']}**", description=f'', color=0x8B4C39)
        embed2 = discord.Embed(title=f"**{result['weapons'][1]['name']}**", description=f'', color=0x8B4C39)
        embed3 = discord.Embed(title=f"**{result['weapons'][2]['name']}**", description=f'', color=0x8B4C39)
        embed4 = discord.Embed(title=f"**{result['weapons'][3]['name']}**", description=f'', color=0x8B4C39)
        embed1.set_thumbnail(url = result['weapons'][0]['image']['url'])
        embed2.set_thumbnail(url = result['weapons'][1]['image']['url'])
        embed3.set_thumbnail(url = result['weapons'][2]['image']['url'])
        embed4.set_thumbnail(url = result['weapons'][3]['image']['url'])

        embeds = [embed, embed1, embed2, embed3, embed4]
    return embeds
        

async def splatoon(ctx, type):
    embeds = await get_splatoon_info(type)
    msg = await ctx.send(embeds=embeds, view=SplatoonButton())
    SPLATOON_INDEX[msg.id] = {'mode': type, 'index': 0}