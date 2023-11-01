from help_functions.help_text import *
from help_functions.help_time import *
from commands.music.cmd_modify import skip
from commands.music.cmd_resume import pause, resume
from commands.music.music_playlist import player



async def current(ctx, msg=None, gpt=False):
    curr_info = player.get_curr(ctx.guild.id)
    if curr_info == {}:
        embed_var = str_no_song_playing
    else:
        title = f'当前播放:\n{curr_info["title"]}\n{time_display(curr_info)} {curr_info["status"]}'
        desc = f'{curr_info["webpage_url"]}'
        embed_var = discord.Embed(title=title, description=desc, color=SUCCESS)
        embed_var.set_image(url=curr_info['thumbnail'])
    
    if msg is None:       msg = await ctx.send(embed=embed_var, view=CurrentButton())
    if gpt and msg is not None: await msg.edit(content = '', embed=embed_var, view=CurrentButton())
    return embed_var



class CurrentButton(discord.ui.View):

    @discord.ui.button(label="⏯", row=0, style=discord.ButtonStyle.primary)
    async def resume_button_callback(self, interaction, button):
        button.view.timeout = None
        curr_info = player.get_curr(interaction.guild.id)
        if curr_info['status'] == '[正在播放]':
            await pause(interaction, interaction.client, interaction.message)
        elif curr_info['status'] == '[已暂停]':
            await resume(interaction, interaction.client, interaction.message)
        embed_var = await current(interaction, msg=interaction.message)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)

    @discord.ui.button(label="跳过", row=0, style=discord.ButtonStyle.success)
    async def skip_button_callback(self, interaction, button):
        button.view.timeout = None
        await skip(interaction, interaction.client, interaction.message)
        embed_var = await current(interaction, msg=interaction.message)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)

    @discord.ui.button(label="刷新", row=0, style=discord.ButtonStyle.success)
    async def refresh_button_callback(self, interaction, button):
        button.view.timeout = None
        embed_var = await current(interaction, msg=interaction.message)
        await interaction.response.edit_message(content = '', embed=embed_var, view=self)

    @discord.ui.button(label="关闭菜单", row=0, style=discord.ButtonStyle.danger)
    async def delete_button_callback(self, interaction, button):
        button.view.timeout = None
        mid = interaction.message.id
        await interaction.channel.purge(limit=100, check=lambda m: m.id == mid)