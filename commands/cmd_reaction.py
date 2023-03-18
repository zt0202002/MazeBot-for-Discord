import discord
from discordhelp import getEmoteFromName
from commands.cmd_queue import update_queue
from commands.cmd_resume import pause, resume
from commands.cmd_skip import skip
from commands.cmd_current import current, CURRENT_ID
from commands.cmd_queue import QUEUE_ID

async def reply_reaction(reaction, user, bot):
    
    # 如果不是用户，或者是bot自己，就不处理
    if user == bot.user:    return

    # 指定表情  

    # queue
    next_page = getEmoteFromName(":arrow_right:")
    prev_page = getEmoteFromName(":arrow_left:")
    refresh = getEmoteFromName(":arrows_counterclockwise:")

    if (reaction.emoji == next_page): await update_queue(reaction.message, 'next')
    elif (reaction.emoji == prev_page): await update_queue(reaction.message, 'prev')
    elif (reaction.emoji == refresh): 
        if reaction.message.id in QUEUE_ID:
            await update_queue(reaction.message, 'refresh')
        elif reaction.message.id in CURRENT_ID:
            await current(reaction.message, bot, reaction.message)

    # song
    pause_button = getEmoteFromName(":pause_button:")
    play = getEmoteFromName(":arrow_forward:")
    skip_button = getEmoteFromName(":track_next:")

    if (reaction.emoji == pause_button): await pause(reaction.message, bot, reaction.message)
    elif (reaction.emoji == play): await resume(reaction.message, bot, reaction.message)
    elif (reaction.emoji == skip_button): await skip(reaction.message, bot, reaction.message)