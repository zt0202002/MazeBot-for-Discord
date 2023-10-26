from help_functions.help_text import *
from help_functions.help_time import *
from commands.music.music_playlist import player
from commands.music.cmd_resume import resume, pause
from commands.music.cmd_skip import skip

PAGE_SIZE = 5

async def queue(ctx, msg=None):
    if msg is None: 
        msg = await ctx.send(embed=str_loading_song)
    embed_var = convert_queue_to_embed(player.get_list(ctx.guild.id), player.get_curr(ctx.guild.id), 0)
    await msg.edit(content = '', embed=embed_var, view=QueueButton())



def convert_queue_to_embed(playlist, curr_info, start, pagesize=PAGE_SIZE):
    if playlist == [] or start > len(playlist): 
        return str_no_song_playing
    
    if start < 0:                       start = 0
    if start+pagesize > len(playlist):  pagesize = len(playlist)-start

    total_time = total_time_display(sum(map(lambda info: info["duration"], playlist)), curr_info)
    embed_var = discord.Embed(title=f'播放列表 共{len(playlist)+1}首 {total_time}\n', description="", color=SUCCESS)

    if curr_info != {}:
        info_row = f'**当前歌曲:\n{curr_info["title"]}\n{time_display(curr_info)} {curr_info["status"]}\n **'
        embed_var.add_field(name=info_row, value=f'', inline=False)
    for i in range(pagesize):
        info_row = f'[{start+i+1}]  {playlist[start+i]["title"][:35]}'
        embed_var.add_field(name=info_row, value=f'', inline=False)
    
    return embed_var





class QueueButton(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self.index = 0
    


    @discord.ui.button(label="<<", row=0, style=discord.ButtonStyle.primary, disabled=False)
    async def first_button_callback(self, interaction, button):
        button.view.timeout = None
        gid = interaction.guild.id
        playlist = player.get_list(gid)

        self.index = 0

        embed_var = convert_queue_to_embed(playlist, player.get_curr(gid), self.index)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)
    


    @discord.ui.button(label="<", row=0, style=discord.ButtonStyle.primary, disabled=False)
    async def prev_button_callback(self, interaction, button):
        button.view.timeout = None
        gid = interaction.guild.id
        playlist = player.get_list(gid)

        self.index = 0 if PAGE_SIZE > self.index else self.index - PAGE_SIZE

        embed_var = convert_queue_to_embed(playlist, player.get_curr(gid), self.index)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)



    @discord.ui.button(label='⏯', row=0, style=discord.ButtonStyle.primary)
    async def resume_button_callback(self, interaction, button):
        button.view.timeout = None
        gid = interaction.guild.id
        playlist = player.get_list(gid)
        curr_info = player.get_curr(gid)

        if curr_info['status'] == '[正在播放]':
            await pause(interaction, interaction.client, interaction.message)
        elif curr_info['status'] == '[已暂停]':
            await resume(interaction, interaction.client, interaction.message)
        
        embed_var = convert_queue_to_embed(playlist, player.get_curr(gid), self.index)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)



    @discord.ui.button(label=">", row=0, style=discord.ButtonStyle.primary, disabled=False)
    async def next_button_callback(self, interaction, button):
        button.view.timeout = None
        gid = interaction.guild.id
        playlist = player.get_list(gid)

        remainder = len(playlist) % PAGE_SIZE
        if self.index + PAGE_SIZE >= len(playlist): self.index = len(playlist) - remainder
        else:                                       self.index+= PAGE_SIZE

        embed_var = convert_queue_to_embed(playlist, player.get_curr(gid), self.index)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)



    @discord.ui.button(label=">>", row=0, style=discord.ButtonStyle.primary, disabled=False)
    async def last_button_callback(self, interaction, button):
        button.view.timeout = None
        gid = interaction.guild.id
        playlist = player.get_list(gid)

        remainder = len(playlist) % PAGE_SIZE
        if remainder == 0:  self.index = len(playlist) - PAGE_SIZE
        else:               self.index = len(playlist) - remainder
        
        embed_var = convert_queue_to_embed(playlist, player.get_curr(gid), self.index)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)
    

    
    @discord.ui.button(label="跳过", row=1, style=discord.ButtonStyle.success)
    async def skip_button_callback(self, interaction, button):
        button.view.timeout = None
        gid = interaction.guild.id
        await skip(interaction, interaction.client, msg=interaction.message)
        playlist = player.get_list(gid)
        
        embed_var = convert_queue_to_embed(playlist, player.get_curr(gid), self.index)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)
        


    @discord.ui.button(label="刷新", row=1, style=discord.ButtonStyle.success)
    async def refresh_button_callback(self, interaction, button):
        button.view.timeout = None
        gid = interaction.guild.id
        playlist = player.get_list(gid)
        
        embed_var = convert_queue_to_embed(playlist, player.get_curr(gid), self.index)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)

        

    @discord.ui.button(label="关闭菜单", row=1, style=discord.ButtonStyle.danger)
    async def delete_button_callback(self, interaction, button):
        button.view.timeout = None
        await interaction.channel.purge(limit=100, check=lambda m: m.id == interaction.message.id)