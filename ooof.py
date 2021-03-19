import discord
from discord.ext import commands, tasks
import re
import asyncio
import json
from datetime import datetime, timedelta
import os
import random

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all(), case_insensitive=True)

with open(r"C:\Users\nakul\Documents\GitHub\mybot\jsons\py.json", 'r') as f:
    bot.data = json.load(f)

with open(r"C:\Users\nakul\Documents\GitHub\mybot\jsons\emoji.json", 'r') as f:
    bot.emoji = json.load(f)

async def save():
    await bot.wait_until_ready()
    while not bot.is_closed():
        with open(r"C:\Users\nakul\Documents\GitHub\mybot\jsons\py.json", 'w') as f:
            json.dump(bot.data, f, indent=4)

        await asyncio.sleep(1)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
bot.admin_roles = ["staff", "Mods"]
bot.server_developer_role = "Server Developers"
bot.TICK_MARK = "<:tick_mark:814801884358901770>"
bot.CROSS_MARK = "<:cross_mark:814801897138815026>"
ban_reason = ""
kicks = False
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
async def trail(context, e: str or discord.Emoji=None):
    print(type(e))
    print(type(str(e)))
    if e not in bot.emoji.values():
        if type(e) == discord.Emoji:
            if context.message.author.id not in bot.data['trail']:
                bot.data['trail'][context.message.author.id] = {}
            bot.data['trail'][context.message.author.id]['emj'] = str(e)
            bot.data['trail'][context.message.author.id]['tog'] = True
        else:
            em = discord.Embed(description=f"{bot.CROSS_MARK} Please use a valid emoji!")
            await context.send(embed=em)
    else:
        if context.message.author.id not in bot.data['trail']:
            bot.data['trail'][context.message.author.id] = {}
        bot.data['trail'][context.message.author.id]['emj'] = e
        bot.data['trail'][context.message.author.id]['tog'] = True


    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['ct', 'rt', 'resolveticket'])
@commands.has_permissions(manage_messages=True)
async def closeticket(context, *, reason: str=None):
    chn = context.channel
    if str(chn) in bot.data['ticket']['val'][str(context.guild.id)]:
        mem = bot.get_user(bot.data['ticket']['val'][str(context.guild.id)][str(chn)])
        em = discord.Embed(description="Resolved your ticket!", timestamp=datetime.utcnow())
        em.add_field(name="Reason", value=reason)
        em.set_footer(text=f"Resolved by {context.message.author}", icon_url=context.message.author.avatar_url)
        await mem.send(embed=em)
        await chn.delete()
        del bot.data['ticket']['val'][str(context.guild.id)][str(chn)]

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
async def suggest(context, *, msg=None):
    chn = bot.get_channel(bot.data['suggest']['chn'][str(context.guild.id)])
    num = bot.data['suggest']['count'][str(context.guild.id)]
    if bot.data['suggest']['chn'][str(context.guild.id)] == "":
        em = discord.Embed(description=f"{bot.CROSS_MARK} This server doesn't have a suggestion channel set up!\n Ask the moderators to run the `$setsuggest` command!", timestamp=datetime.utcnow())
        await context.send(embed=em)
        return
    else:
        if msg != None:
            em = discord.Embed(title=f"Suggestion #{num}", description=msg)
            em.set_author(name=context.message.author, icon_url=context.message.author.avatar_url)
            m1 =  await chn.send(embed=em)
            await m1.add_reaction(f"{bot.TICK_MARK}")
            await m1.add_reaction(f"{bot.CROSS_MARK}")
            await context.message.delete()
            em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully sent suggestion!")
            mes = await context.send(embed=em)
            await asyncio.sleep(5)
            await mes.delete()
            bot.data['suggest']['val'][str(context.guild.id)][str(num)] = {}
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['author'] = str(context.message.author)
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['msg'] = str(msg)
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['icon'] = str(context.message.author.avatar_url)
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['link'] = str(m1.jump_url)
            bot.data['suggest']['count'][str(context.guild.id)] = bot.data['suggest']['count'][str(context.guild.id)] + 1
        else:
            em = discord.Embed(description=f"{bot.TICK_MARK} Please type your suggestion now!")
            mess = await context.send(embed=em)
            def check(m):
                return m.author == context.message.author and m.channel == context.channel
            try:
                msgg = await bot.wait_for('message', timeout= 30, check=check)
                await mess.delete()
            except asyncio.TimeoutError:
                em = discord.Embed(description=f"{bot.CROSS_MARK} You ran out of time! Please re-type the command!")
                await context.channel.send(embed=em)
                return
            msg = msgg.content
            em = discord.Embed(title=f"Suggestion #{num}", description=msg)
            em.set_author(name=context.message.author, icon_url=context.message.author.avatar_url)
            m1 =  await chn.send(embed=em)
            await m1.add_reaction(f"{bot.TICK_MARK}")
            await m1.add_reaction(f"{bot.CROSS_MARK}")
            await context.message.delete()
            await msgg.delete()
            em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully sent suggestion!")
            mes = await context.send(embed=em)
            await asyncio.sleep(5)
            await mes.delete()
            bot.data['suggest']['val'][str(context.guild.id)][str(num)] = {}
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['author'] = str(context.message.author)
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['msg'] = str(msg)
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['icon'] = str(context.message.author.avatar_url)
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['link'] = str(m1.jump_url)
            bot.data['suggest']['count'][str(context.guild.id)] = bot.data['suggest']['count'][str(context.guild.id)] + 1

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def approve(context, no=None, *, reason=None):
    log_chat = bot.get_channel(bot.data['suggest']['chn'][str(context.guild.id)])
    if str(no) in bot.data['suggest']['val'][str(context.guild.id)]:
        em = discord.Embed(title=f'Approved suggestion #{str(no)}', color=discord.Color.green(), timestamp=datetime.utcnow())
        em.add_field(name=f"Suggestion content", value=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['msg'] + f" - [Suggestion!]({bot.data['suggest']['val'][str(context.guild.id)][str(no)]['link']})", inline=False)
        em.add_field(name=f"Reason from {context.message.author.name}", value=reason, inline=False)
        em.set_author(name=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['author'], icon_url=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['icon'])
        await log_chat.send(embed=em)
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Approved suggestion #{str(no)} for reason - {reason}!")
        ems = await context.send(embed=em)
        await context.message.delete()
        await asyncio.sleep(5)
        await ems.delete()
        return
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> Please provide a valid suggestion ID!")
        await context.channel.send(embed=em)
        return

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def deny(context, no=None, *, reason=None):
    log_chat = bot.get_channel(bot.data['suggest']['chn'][str(context.guild.id)])
    if str(no) in bot.data['suggest']['val'][str(context.guild.id)]:
        em = discord.Embed(title=f'Denied suggestion #{str(no)}', color=discord.Color.red(), timestamp=datetime.utcnow())
        em.add_field(name=f"Suggestion content", value=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['msg'] + f" - [Suggestion!]({bot.data['suggest']['val'][str(context.guild.id)][str(no)]['link']})", inline=False)
        em.add_field(name=f"Reason from {context.message.author.name}", value=reason, inline=False)
        em.set_author(name=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['author'], icon_url=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['icon'])
        await log_chat.send(embed=em)
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Denied suggestion #{str(no)} for reason - {reason}!")
        ems = await context.send(embed=em)
        await context.message.delete()
        await asyncio.sleep(5)
        await ems.delete()
        return
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> Please provide a valid suggestion ID!")
        await context.channel.send(embed=em)
        return

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def consider(context, no=None, *, reason=None):
    log_chat = bot.get_channel(bot.data['suggest']['chn'][str(context.guild.id)])
    if str(no) in bot.data['suggest']['val'][str(context.guild.id)]:
        em = discord.Embed(title=f'Considered suggestion #{str(no)}', color=discord.Color.blue(), timestamp=datetime.utcnow())
        em.add_field(name=f"Suggestion content", value=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['msg'] + f" - [Suggestion!]({bot.data['suggest']['val'][str(context.guild.id)][str(no)]['link']})", inline=False)
        em.add_field(name=f"Reason from {context.message.author.name}", value=reason, inline=False)
        em.set_author(name=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['author'], icon_url=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['icon'])
        await log_chat.send(embed=em)
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Considered suggestion #{str(no)} for reason - {reason}!")
        ems = await context.send(embed=em)
        await context.message.delete()
        await asyncio.sleep(5)
        await ems.delete()
        return
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> Please provide a valid suggestion ID!")
        await context.channel.send(embed=em)
        return

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def implement(context, no=None, *, reason=None):
    log_chat = bot.get_channel(bot.data['suggest']['chn'][str(context.guild.id)])
    if str(no) in bot.data['suggest']['val'][str(context.guild.id)]:
        em = discord.Embed(title=f'Implemented suggestion #{str(no)}', color=discord.Color.purple(), timestamp=datetime.utcnow())
        em.add_field(name=f"Suggestion content", value=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['msg'] + f" - [Suggestion!]({bot.data['suggest']['val'][str(context.guild.id)][str(no)]['link']})", inline=False)
        em.add_field(name=f"Reason from {context.message.author.name}", value=reason, inline=False)
        em.set_author(name=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['author'], icon_url=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['icon'])
        await log_chat.send(embed=em)
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Implemented suggestion #{str(no)} for reason - {reason}!")
        ems = await context.send(embed=em)
        await context.message.delete()
        await asyncio.sleep(5)
        await ems.delete()
        return
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> Please provide a valid suggestion ID!")
        await context.channel.send(embed=em)
        return

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def setl(context, channel: discord.TextChannel=None):
    if channel == None:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You must provide a channel for this command!")
        await context.send(embed=em)
    else:
        bot.data['logs'][str(context.guild.id)] = channel.id
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully set logs channel as - {channel.mention}!", timestamp=datetime.utcnow())
        mes = await context.send(embed=em)
        await asyncio.sleep(5)
        await context.message.delete()
        await mes.delete()


    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['setwidt'])
@commands.has_permissions(manage_messages=True)
async def setw(context, channel: discord.TextChannel=None):
    if channel == None:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You must provide a channel for this command!")
        await context.send(embed=em)
    else:
        bot.data['widt'][str(context.guild.id)] = channel.id
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully set widt channel as - {channel.mention}!", timestamp=datetime.utcnow())
        mes = await context.send(embed=em)
        await asyncio.sleep(5)
        await context.message.delete()
        await mes.delete()

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['setsuggest'])
@commands.has_permissions(manage_messages=True)
async def sets(context, channel: discord.TextChannel=None):
    if channel == None:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You must provide a channel for this command!")
        await context.send(embed=em)
    else:
        bot.data['suggest']['chn'][str(context.guild.id)] = channel.id
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully set suggestions channel as - {channel.mention}!", timestamp=datetime.utcnow())
        mes = await context.send(embed=em)
        await asyncio.sleep(5)
        await context.message.delete()
        await mes.delete()

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['setticket'])
@commands.has_permissions(manage_messages=True)
async def sett(context, channel: discord.TextChannel=None):
    if channel == None:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You must provide a channel for this command!")
        await context.send(embed=em)
    else:
        bot.data['ticket']['chn'][str(context.guild.id)] = channel.id
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully set ticket channel as - {channel.mention}!", timestamp=datetime.utcnow())
        mes = await context.send(embed=em)
        em = discord.Embed(title="Create ticket!", description="React 📩 to create a ticket!")
        msg = await channel.send(embed=em)
        await msg.add_reaction('📩')
        await channel.set_permissions(context.guild.default_role, send_messages = False, read_messages = True)
        bot.data['ticket']['msg'][str(context.guild.id)] = msg.id
        await asyncio.sleep(5)
        await context.message.delete()
        await mes.delete()
        await context.guild.create_category_channel(name='tickets')

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['setticketadmin'])
@commands.has_permissions(manage_messages=True)
async def setta(context, role: discord.Role=None):
    if role == None:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You must provide a role for this command!")
        await context.send(embed=em)
    else:
        bot.data['ticket']['staff'][str(context.guild.id)] = str(role.id)
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully set staff role as - {role.mention}")
        mes = await context.send(embed=em)
        await asyncio.sleep(5)
        await context.message.delete()
        await mes.delete()

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['resetsuggest'])
@commands.has_permissions(manage_messages=True)
async def resets(context):
    em = discord.Embed(description=f"{bot.CROSS_MARK} Are you sure you want to reset the suggestion count?\n Type yes to proceed!")
    msgg = await context.send(embed=em)
    def check(m):
        return m.author == context.message.author and m.channel == context.channel
    try:
        msg = await bot.wait_for('message', timeout= 30, check=check)
    except asyncio.TimeoutError:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You ran out of time! Please re-type the command!")
        await context.channel.send(embed=em)
        return
    if msg.content.upper() == 'YES':
        bot.data['suggest']['count'][str(context.guild.id)] = 1
        bot.data['suggest']['val'][str(context.guild.id)] = {}

        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully reset suggestion count!")
        mes = await context.send(embed=em)
        await context.message.delete()
        await msg.delete()
        await asyncio.sleep(5)
        await mes.delete()
        await msgg.delete()
    else:
        em = discord.Embed(description=f"{bot.CROSS_MARK} Process cancelled!")
        mes = await context.channel.send(embed=em)
        await context.message.delete()
        await msg.delete()
        await asyncio.sleep(5)
        await mes.delete()
        await msgg.delete()
        return

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['resetticket'])
@commands.has_permissions(manage_messages=True)
async def resett(context):
    em = discord.Embed(description=f"{bot.CROSS_MARK} Are you sure you want to reset the ticket count?\n Type yes to proceed!")
    msgg = await context.send(embed=em)
    def check(m):
        return m.author == context.message.author and m.channel == context.channel
    try:
        msg = await bot.wait_for('message', timeout= 30, check=check)
    except asyncio.TimeoutError:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You ran out of time! Please re-type the command!")
        await context.channel.send(embed=em)
        return
    if msg.content.upper() == 'YES':
        bot.data['ticket']['count'][str(context.guild.id)] = 1
        bot.data['ticket']['val'][str(context.guild.id)] = {}
        bot.data['ticket']['msg'][str(context.guild.id)] = ""
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully reset ticket count!")
        mes = await context.send(embed=em)
        await context.message.delete()
        await msg.delete()
        await asyncio.sleep(5)
        await mes.delete()
        await msgg.delete()
    else:
        em = discord.Embed(description=f"{bot.CROSS_MARK} Process cancelled!")
        mes = await context.channel.send(embed=em)
        await context.message.delete()
        await msg.delete()
        await asyncio.sleep(5)
        await mes.delete()
        await msgg.delete()
        return

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# on message event handler - handles a lot of the anti blocking, logging. - Even Recieves all messages,
# including DMs and from itself
@bot.event
async def on_message(msg):

    # ignore it if its the bots own message
    if msg.author.id == bot.user.id:
        return

    # get main log channel
    try:
        chn = bot.get_channel(bot.data['logs'][str(msg.guild.id)])
    except AttributeError:
        # It is a DM channel message - It has no guild
        pass
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # TICKET LOGGER
    try:
        # get all currently open tickets
        curr_open_tickets = bot.tickets_collection.find({"GUILD_ID": msg.guild.id, "STATUS": "OPEN"})
        # get the channel ids of those tickets
        currtickids = [i["CHN_ID"] for i in curr_open_tickets]

        # check if the channel id of the message was in this list
        if msg.channel.id in currtickids:
            # log the message with details into mongodb
            d = {"time": msg.created_at, "authorid": msg.author.id,
                 "authorname": f'{msg.author.name}#{msg.author.discriminator}', 'content': msg.content}
            if msg.attachments:
                d["attachments"] = True
            else:
                d["attachments"] = False

            bot.tickets_collection.update_one({"GUILD_ID": msg.guild.id, "CHN_ID": msg.channel.id},
                                              {"$addToSet": {"CHAT_LOG": d}})
    except AttributeError:
        # DM channel - it has no guild attribute.
        pass
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ATTACHMENT LOGGER
    if msg.attachments and not isinstance(msg.channel, discord.channel.DMChannel):  # only log non DMs

        # get date time of message creation
        t = datetime.strftime(msg.created_at,
                                '%d/%m/%Y, %H:%M:%S')

        # send a new log message for each attachment in the msg
        for i in msg.attachments:
            # usually len 1, just in case...

            # generate message
            em = discord.Embed(description=f"**Attachment sent in {str(msg.channel.mention)}** - [Message]({msg.jump_url})", color=discord.Color.blue())
            em.add_field(name='Author', value=msg.author, inline=False)
            if msg.content == '':
                em.add_field(name='Message', value=f"{bot.CROSS_MARK} No message!")
            else:
                em.add_field(name='Message', value=msg.content)
            em.add_field(name='Channel', value=msg.channel.mention)
            em.add_field(name='Time', value=t)
            em.add_field(name='Link', value=i.url, inline=False)
            await chn.send(embed=em)

            if i.size < 8000000:  # 8 MB in bytes
                # can send attachment
                fi = await i.to_file()
                await chn.send('File:', file=fi)
            else:
                # cant send attachment, too large!
                await chn.send('File:'+"\n**Couldn't Log attachment - Too large (Larger than 8000000 Bytes)**\n")
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # return prefix if bot is tagged (tag must be first in the msg)
    if msg.content.startswith(f"<@!{bot.user.id}>"):
        await msg.channel.send(f"Hey there, my prefix is {bot.command_prefix}")

    # process the message normally (as in command)
    await bot.process_commands(msg)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# The edit event - all message edits are detected here
@bot.event
async def on_message_edit(before, after):

    try:
        chn = bot.get_channel(bot.common_server_info_collection.find_one({"SERVER_ID": after.guild.id})["LOG_CHANNEL"])
    except AttributeError:
        # DM channel - there is none guild attribute for Message
        pass

    # Invite block for edits
    if after.content.find("discord.gg") != -1 and not isinstance(after.channel, discord.channel.DMChannel):
        if before.author == bot.user:
            return
        # found discord.gg!
        ind = after.content.find("discord.gg")
        if after.content[ind + len("discord.gg"):] \
                == "/jDMYEV5":
            pass
        else:
            # found discord.gg!
            em = discord.Embed(description=f"{bot.CROSS_MARK}  You can not send invite links!")

            await after.channel.send(embed=em)
            await chn.send(f"{after.author.mention} | {after.author.id} did a EDIT invite in {after.channel}.")
            await after.delete()
    elif after.content.find("discordapp.com/invite") != -1 and not isinstance(after.channel, discord.channel.DMChannel):
        # found "discordapp.com/invite"
        ind = after.content.find("discordapp.com/invite")
        if after.content[ind + len("discordapp.com/invite"):] == "/jDMYEV5":
            pass
        else:
            # found discord.gg!
            em = discord.Embed(description=f"{bot.CROSS_MARK}  You can not send invite links!")
            await after.channel.send(embed=em)    
            await chn.send(f"{after.author.mention} | {after.author.id} did a EDIT invite in {after.channel}.")
            await after.delete()
    elif after.content.find("discord.com/invite") != -1 and not isinstance(after.channel, discord.channel.DMChannel):
        # found "discord.com/invite"
        ind = after.content.find("discord.com/invite")
        if after.content[ind + len("discord.com/invite"):] == "/jDMYEV5":
            pass
        else:
            # found discord.gg!
            em = discord.Embed(description=f"{bot.CROSS_MARK}  You can not send invite links!")
            await after.channel.send(embed=em) 
            await chn.send(f"{after.author.mention} | {after.author.id} did a EDIT invite in {after.channel}.")
            await after.delete()

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Master command ERROR HANDLER!
@bot.event
async def on_command_error(ctx, error):
    # ignore command not found errors
    ignored = (commands.CommandNotFound)

    if isinstance(error, ignored):
        return

    # handle Cooldown's
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            await ctx.send(f'You must wait {int(s)} second(s) to use this command')
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f'You must wait {int(m)} minute(s) and {int(s)} second(s) to use this command')
        else:
            await ctx.send(
                f'You must wait {int(h)} hour(s), {int(m)} minute(s) and {int(s)} second(s) to use this command')
        return
    # Handle wrong user input - missing arguments etc.
    elif isinstance(error, commands.UserInputError):
        await ctx.send(f'Please use the command properly:\n```{error}```')
        return
    # Handle permission issues (check failures)
    elif isinstance(error, commands.CheckFailure):
        em = discord.Embed(description=f"{bot.CROSS_MARK}  You lack the required permissions!")
        await ctx.send(embed=em)
        return
    # handle unhandled errors - just raise it and send to discord.
    else:
        if error == None:
            return
        await ctx.send(f"Internal Error!\n```{error}```\nPlease inform the moderators immediately.")
        raise error

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="whoami")
async def whoami(context):
    channel = context.message.channel
    author = context.message.author
    await channel.send("Hi, you are " + str(author.mention) + " and you are talking to **The Oracle** a bot made for **The Matrix**!! You are currently in the channel : " + str(channel.mention))
    await context.message.author.send("You can not let the other members on the server know about this... Its top secret stuff - you are an amazing person!! : )")

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="ONION")
async def onion(context):
    await context.send("https://cdn.discordapp.com/attachments/774156001993162793/814833307836481576/images.png")

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="kick", pass_context = True)
@commands.has_permissions(kick_members=True)
async def kick(context, member: discord.Member, *, reason=None):
    global kicks
    kicks = True
    for_reason = "For reason - "
    log_chat = bot.get_channel(bot.data['logs'][str(context.guild.id)])
    if reason == None:
        reason = "No reason provided! by moderator " + str(context.message.author)
    if reason != "No reason provided! by moderator " + str(context.message.author):
        reason = reason + "! by moderator " + str(context.message.author)
    if context.message.author != member:
        if kicks == True:
            await member.kick(reason=reason)
            emk = discord.Embed(description=f"**Member kicked**\n {member.mention}", color=discord.Color.red(), timestamp=datetime.utcnow())
            emk.add_field(name="Reason", value=reason)
            emk.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
            emk.set_thumbnail(url=member.avatar_url)
            await log_chat.send(embed=emk)
        if reason == "No reason provided! by moderator " + str(context.message.author):
            for_reason = ""
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Succesfully Kicked {member.mention} \n{for_reason} {str(reason)}", timestamp=datetime.utcnow())
        await context.send(embed=em)
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> You cannot kick yourself!", timestamp=datetime.utcnow())
        await context.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="ban", pass_context = True)
@commands.has_permissions(ban_members=True)
async def ban(context, user: discord.User, *, reason=None):
    global ban_reason
    for_reason = "For reason - "
    if reason == None:
        reason = "No reason provided! by moderator " + str(context.message.author)
    if reason != "No reason provided! by moderator " + str(context.message.author):
        reason = reason + "! by moderator " + str(context.message.author)
    ban_reason = str(reason)
    if context.message.author != user:
        await context.guild.ban(user, delete_message_days=7, reason=reason)
        if reason == "No reason provided! by moderator " + str(context.message.author):
            for_reason = ""
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Succesfully Banned {user.mention} \n{for_reason}{str(reason)}")
        await context.send(embed=em)
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> You cannot ban yourself!")
        await context.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['ui', 'info', 'i'])
async def userinfo(context, *, user: discord.Member = None):
    if isinstance(context.channel, discord.DMChannel):
        return    
    if user is None:
        user = context.author
    date_format = "%a, %d %b %Y %I:%M %p"
    em = discord.Embed(title=str(user.display_name) + "'s User Information", color=discord.Color.blue(), description=user.mention, timestamp=datetime.utcnow())
    em.set_thumbnail(url=user.avatar_url)
    em.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(context.guild.members, key=lambda m: m.joined_at)
    em.add_field(name="Join position", value=str(members.index(user)+1))
    em.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
    m = 16
    if len(user.roles) > m:
        role_string = "Too many to list! <:whathasyoudone:796680789881389146>"
    em.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string)
    em.add_field(name="Bot", value=user.bot)
    verified = not user.pending
    em.add_field(name="Verified", value=str(verified))
    em.set_footer(text='USER ID: ' + str(user.id))
    await context.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['si', 'gi', 'guildinfo'])
async def serverinfo(context):
    name = str(context.guild.name)
    owner = str(context.guild.owner)
    id = str(context.guild.id)
    memberCount = str(context.guild.member_count)
    roleCount = str(len(context.guild.roles))
    channelCount = str(len(context.guild.channels))
    textCount = str(len(context.guild.text_channels))
    voiceCount = str(len(context.guild.voice_channels))
    catcount = str(len(context.guild.categories))
    icon = str(context.guild.icon_url)  
    em = discord.Embed(title=name + " Server Information",color=discord.Color.blue(), timestamp=datetime.utcnow())
    em.set_thumbnail(url=icon)
    em.add_field(name="Owner", value=owner, inline=True)
    em.add_field(name="Level", value=f"{context.guild.premium_tier} ({context.guild.premium_subscription_count}/30)", inline=True)
    em.add_field(name="Pewpie Bot", value="<:tick_mark:814801884358901770> True", inline=True)
    em.add_field(name="Member Count", value=memberCount, inline=True)
    em.add_field(name="Role Count", value=roleCount, inline=True)
    em.add_field(name="Channel Count", value=f"{channelCount} (<:text:819265166231339008> {textCount}, <:voice:819265155870228551> {voiceCount})\nCategories - {catcount}", inline=True)
    if hasattr(context.guild.rules_channel, "mention"):
        em.add_field(name="Rules", value=f"{context.guild.rules_channel.mention}", inline=True)
    if bot.data['suggest']['chn'][str(context.guild.id)] != "":
        chn = bot.get_channel(bot.data['suggest']['chn'][str(context.guild.id)])
        em.add_field(name="Suggestions channel", value=f"{chn.mention}", inline=True)
    if bot.data['ticket']['chn'][str(context.guild.id)] != "":
        chn = bot.get_channel(bot.data['ticket']['chn'][str(context.guild.id)])
        em.add_field(name="Ticketing channel", value=f"{chn.mention}", inline=True)
    em.set_image(url=context.guild.banner_url)
    em.set_footer(text="Server ID : " + id)
    await context.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["ci", "channeli", "cinfo"])
async def channelinfo(context, *, channel: discord.TextChannel=None):
    date_format = "%a, %d %b %Y %I:%M %p"
    roles = ""
    if channel == None:
        channel = context.channel
    if isinstance(context.channel, discord.DMChannel):
        return
    em = discord.Embed(title=channel.name + " Channel Information", color=discord.Color.blue(), timestamp=datetime.utcnow())
    em.add_field(name="Category", value=channel.category)
    em.add_field(name="Created at", value=channel.created_at.strftime(date_format))
    em.add_field(name="Position", value=channel.position)
    if channel.category != None:
        em.add_field(name="Synced", value=channel.permissions_synced)   
    em.add_field(name="Slowmode", value=channel.slowmode_delay)
    for role in channel.changed_roles:
        roles += f"{str(role.mention)}\n"
    if roles != "":
        em.add_field(name="Overwritten Roles", value=str(roles))
    else:
        em.add_field(name="Overwritten Roles", value="None")
    em.set_thumbnail(url=context.guild.icon_url)
    await context.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["ri", "rolei", "rinfo"])
async def roleinfo(context, *, role: discord.Role=None):
    tagss = role.tags
    date_format = "%a, %d %b %Y %I:%M %p"
    if role == None:
        eme = discord.Embed(description=f"<:cross_mark:814801897138815026> You must provide a role for this command!")
        await context.send(embed=eme)
    else:
        em = discord.Embed(title=role.name + " Role Information", color=discord.Color.blue(), timestamp=datetime.utcnow())
        em.add_field(name="Color", value=str(role.color))
        em.add_field(name="Created at", value=str(role.created_at.strftime(date_format)))
        em.add_field(name="Position", value=str(role.position))
        em.add_field(name="Members", value=str(len(role.members)))
        em.add_field(name="Displayed", value=str(role.hoist))
        if hasattr(tagss, 'is_premium_subscriber') == True and hasattr(tagss, 'is_bot_managed') == True:
                em.add_field(name="Boost role/Bot role", value=str(role.tags.is_premium_subscriber()) + "/" + str(role.tags.is_bot_managed()))
        em.set_thumbnail(url=context.guild.icon_url)
    await context.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
async def purge(context, limit=5, member: discord.Member=None):
    await context.message.delete()
    msg = []
    try:
        limit = int(limit)
    except:
        return await context.send("Please pass in an integer as limit")
    if not member:
        await context.channel.purge(limit=limit)
        return await context.send(f"Purged {limit} messages", delete_after=5)
    async for m in context.channel.history():
        if len(msg) == limit:
            break
        if m.author == member:
            msg.append(m)
    await context.channel.delete_messages(msg)
    await context.send(f"Purged {limit} messages of {member.mention}", delete_after=3)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["a", "av"])
async def avatar(context, member: discord.User=None):
    if member == None:
        member = context.message.author 
    em = discord.Embed(description=f"[Avatar]({member.avatar_url})", color=discord.Color.blue(), timestamp=datetime.utcnow())
    em.set_image(url=member.avatar_url)
    em.set_author(name=str(member), icon_url=member.avatar_url)
    em.set_footer(text="USER ID: " + str(member.id))
    await context.channel.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["servericon"])
async def icon(context):
    em = discord.Embed(title="Icon", color=discord.Color.blue(), timestamp=datetime.utcnow())
    em.set_image(url=context.guild.icon_url)
    em.set_author(name=str(context.message.author), icon_url=context.message.author.avatar_url)
    em.set_footer(text="SERVER ID: " + str(context.guild.id))
    await context.channel.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["serverbanner"])
async def banner(context):
    em = discord.Embed(title="Banner", color=discord.Color.blue(), timestamp=datetime.utcnow())
    em.set_image(url=context.guild.banner_url)
    em.set_author(name=str(context.message.author), icon_url=context.message.author.avatar_url)
    em.set_footer(text="SERVER ID: " + str(context.guild.id))
    await context.channel.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["owo"])
async def owofy(context, *, message: str=None):
    if message == None:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> You must provide text!")
        await context.send(embed=em)
        return
    if "l" in str(message):
        message = message.replace("l", "w")
    elif "r" in str(message):
        message = message.replace("r", "w")
    elif "na" in str(message):
        message = message.replace("na", "nya")
    await context.channel.send(message)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print("------")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("The wait for $"))
    msg1.start()
    msg2.start()
    msg3.start()
    msg4.start()


# Message 1
@tasks.loop(hours=24)
async def msg1():
    chn = bot.get_channel(821293030614368286)
    if bot.data['wt']['sport']['id'] != 0:
        msggggg = await chn.fetch_message(bot.data['wt']['sport']['id'])
        await msggggg.delete()
        bot.data['wt']['sport']['id'] = 0

    if bot.data['wt']['sport']['id2'] != 0:
        msggggggg = await chn.fetch_message(bot.data['wt']['sport']['id2'])
        await msggggggg.delete()
        bot.data['wt']['sport']['id2'] = 0


    bot.data['wt']['sport']["votes"]['bb'] = 0
    bot.data['wt']['sport']['votes']['fb'] = 0
    bot.data['wt']['sport']['votes']['bm'] = 0
    bot.data['wt']['sport']['votes']['cr'] = 0
    bot.data['wt']['sport']['votes']['tt'] = 0
    bot.data['wt']['sport']['reactants'] = {}
    chn = bot.get_channel(821293030614368286)
    em = discord.Embed(title="What sport would you like to play tomorrow?", description="React :basketball: for basketball, \nReact :soccer: for football, \nReact :badminton: for badminton, \nReact :cricket_game: for cricket, \nReact :ping_pong: for table tennis!")
    mes = await chn.send('@everyone', embed=em)
    await mes.add_reaction("🏀")
    await mes.add_reaction("⚽")
    await mes.add_reaction("🏸")
    await mes.add_reaction("🏏")
    await mes.add_reaction("🏓")
    await mes.add_reaction(bot.CROSS_MARK)
    bot.data['wt']['sport']['id'] = mes.id
    await save()

@msg1.before_loop
async def before_msg1():
    for _ in range(60*60*24):
        if datetime.now().hour == 22 and datetime.now().minute == 0:
            return
        await asyncio.sleep(1)

# Message 2
@tasks.loop(hours=24)
async def msg2():
    chn = bot.get_channel(821293030614368286)
    ping = ""
    sport = ""
    for mem in bot.data['wt']['sport']['reactants'].keys():
        ping += mem + " "
    lst = bot.data['wt']['sport']['votes'].values()
    val = max(lst)
    for vote in bot.data['wt']['sport']['votes'].keys():
        if bot.data['wt']['sport']['votes'][vote] == val:
            sport += vote
            if 'bb' in sport:
                sport = sport.replace('bb', '<:bb:822075825134239744> Basketball')
            if 'fb' in sport:
                sport = sport.replace('fb', '<:ftbl:822076629156364318> Football')
            if 'bm' in sport:
                sport = sport.replace('bm', '<:bdm:822076228764827678> Badminton')
            if 'cr' in sport:
                sport = sport.replace('cr', '<:crick:822076976478289990> Cricket')
            if 'tt' in sport:
                sport = sport.replace('tt', ':ping_pong::ping_pong: Table Tennis')
    sport = sport
    em = discord.Embed(title="Sport for Today!", description=f"The sport picked for today is - {sport} with {val} votes!")
    mssg = await chn.send(f"{ping} - {str(len(bot.data['wt']['sport']['reactants'].keys()))}", embed=em)
    bot.data['wt']['sport']['id2'] = mssg.id
    await asyncio.sleep(5)
    if len(sport) == 78:
        s1 = sport[0:33]
        s2 = sport[34:77]
        s = [s1, s2]
        await chn.send(f"Since there was a tie of 2 sports, initiating randomizer!")
        em = discord.Embed(title="Sport for Today!", description=f"The sport picked for today is - {random.choice(s)}!")
        mssge = await chn.send(f"{ping} - {str(len(bot.data['wt']['sport']['reactants'].keys()))}", embed=em)
        bot.data['wt']['sport']['id2'] = mssge.id
        await mssg.delete()
    elif len(sport) == 112:
        s1 = sport[0:33]
        s2 = sport[34:77]
        s3 = sport[78:111]
        s = [s1, s2, s3]
        await chn.send(f"Since there was a tie of 3 sports, initiating randomizer!")
        em = discord.Embed(title="Sport for Today!", description=f"The sport picked for today is - {random.choice(s)}!")
        mssge = await chn.send(f"{ping} - {str(len(bot.data['wt']['sport']['reactants'].keys()))}", embed=em)
        bot.data['wt']['sport']['id2'] = mssge.id
        await mssg.delete()
    elif len(sport) == 156:
        s1 = sport[0:33]
        s2 = sport[34:77]
        s3 = sport[78:111]
        s4 = sport[112:155]
        s = [s1, s2, s3, s4]
        await chn.send(f"Since there was a tie of 4 sports, initiating randomizer!")
        em = discord.Embed(title="Sport for Today!", description=f"The sport picked for today is - {random.choice(s)}!")
        mssge = await chn.send(f"{ping} - {str(len(bot.data['wt']['sport']['reactants'].keys()))}", embed=em)
        bot.data['wt']['sport']['id2'] = mssge.id
        await mssg.delete()
    elif len(sport) == 190:
        s1 = sport[0:33]
        s2 = sport[34:77]
        s3 = sport[78:111]
        s4 = sport[112:155]
        s5 = sport[156:189]
        s = [s1, s2, s3, s4, s5]
        await chn.send(f"Since there was a tie of 5 sports, initiating randomizer!")
        em = discord.Embed(title="Sport for Today!", description=f"The sport picked for today is - {random.choice(s)}!")
        mssge = await chn.send(f"{ping} - {str(len(bot.data['wt']['sport']['reactants'].keys()))}", embed=em)
        bot.data['wt']['sport']['id2'] = mssge.id
        await mssg.delete()


@msg2.before_loop
async def before_msg2():
    for _ in range(60*60*24):
        if datetime.now().hour == 18 and datetime.now().minute == 0:
            return
        await asyncio.sleep(1)


# Message 3
@tasks.loop(hours=24)
async def msg3():
    chn = bot.get_channel(821293030614368286)
    if bot.data['wt']['time']['id'] != 0:
        msggggg = await chn.fetch_message(bot.data['wt']['time']['id'])
        await msggggg.delete()
        bot.data['wt']['time']['id'] = 0

    if bot.data['wt']['time']['id2'] != 0:
        msggggggg = await chn.fetch_message(bot.data['wt']['time']['id2'])
        await msggggggg.delete()
        bot.data['wt']['time']['id2'] = 0


    bot.data['wt']['time']["votes"]['65'] = 0
    bot.data['wt']['time']['votes']['70'] = 0
    bot.data['wt']['time']['votes']['75'] = 0
    bot.data['wt']['time']['votes']['80'] = 0
    bot.data['wt']['time']['votes']['85'] = 0
    bot.data['wt']['time']['reactants'] = {}
    chn = bot.get_channel(821293030614368286)
    em = discord.Embed(title="What time would you like to play tomorrow?", description="React :clock630: for 6:30, \nReact :clock7: for 7:00, \nReact :clock730: for 7:30, \nReact :clock8: for 8:00, \nReact :clock830: for 8:30!")
    mes = await chn.send('@everyone', embed=em)
    await mes.add_reaction("🕡")
    await mes.add_reaction("🕖")
    await mes.add_reaction("🕢")
    await mes.add_reaction("🕗")
    await mes.add_reaction("🕣")
    await mes.add_reaction(bot.CROSS_MARK)
    bot.data['wt']['time']['id'] = mes.id
    await save()

@msg3.before_loop
async def before_msg3():
    for _ in range(60*60*24):
        if datetime.now().hour == 22 and datetime.now().minute == 1:
            return
        await asyncio.sleep(1)

# Message 4
@tasks.loop(hours=24)
async def msg4():
    chn = bot.get_channel(821293030614368286)
    ping = ""
    time = ""
    for mem in bot.data['wt']['time']['reactants'].keys():
        ping += mem
    lst = bot.data['wt']['time']['votes'].values()
    val = max(lst)
    for vote in bot.data['wt']['time']['votes'].keys():
        if bot.data['wt']['time']['votes'][vote] == val:
            time += vote
            if '65' in time:
                time = time.replace('65', '🕡 6:30')
            if '70' in time:
                time = time.replace('70', '🕖 7:00')
            if '75' in time:
                time = time.replace('75', '🕢 7:30')
            if '80' in time:
                time = time.replace('80', '🕗 8:00')
            if '85' in time:
                time = time.replace('85', '🕣 8:30')
    sport = time
    em = discord.Embed(title="Time for today!", description=f"The time picked for today is - {sport} with {val} votes!")
    mssg = await chn.send(f"{ping} - {str(len(bot.data['wt']['time']['reactants'].keys()))}", embed=em)
    bot.data['wt']['time']['id2'] = mssg.id
    await asyncio.sleep(5)
    if len(sport) == 12:
        s1 = sport[0:5]
        s2 = sport[6:11]
        s = [s1, s2]
        await chn.send(f"Since there was a tie of 2 sports, initiating randomizer!")
        em = discord.Embed(title="Time for Today!", description=f"The time picked for today is - {random.choice(s)}!")
        mssge = await chn.send(f"{ping} - {str(len(bot.data['wt']['time']['reactants'].keys()))}", embed=em)
        bot.data['wt']['time']['id2'] = mssge.id
        await mssg.delete()
    elif len(sport) == 18:
        s1 = sport[0:5]
        s2 = sport[6:11]
        s3 = sport[12:17]
        s = [s1, s2, s3]
        await chn.send(f"Time there was a tie of 3 sports, initiating randomizer!")
        em = discord.Embed(title="Sport for Today!", description=f"The time picked for today is - {random.choice(s)}!")
        mssge = await chn.send(f"{ping} - {str(len(bot.data['wt']['time']['reactants'].keys()))}", embed=em)
        bot.data['wt']['time']['id2'] = mssge.id
        await mssg.delete()
    elif len(sport) == 24:
        s1 = sport[0:5]
        s2 = sport[6:11]
        s3 = sport[12:17]
        s4 = sport[18:23]
        s = [s1, s2, s3, s4]
        await chn.send(f"Time there was a tie of 4 sports, initiating randomizer!")
        em = discord.Embed(title="Sport for Today!", description=f"The time picked for today is - {random.choice(s)}!")
        mssge = await chn.send(f"{ping} - {str(len(bot.data['wt']['time']['reactants'].keys()))}", embed=em)
        bot.data['wt']['time']['id2'] = mssge.id
        await mssg.delete()
    elif len(sport) == 30:
        s1 = sport[0:5]
        s2 = sport[6:11]
        s3 = sport[12:17]
        s4 = sport[18:23]
        s5 = sport[24:29]
        s = [s1, s2, s3, s4, s5]
        await chn.send(f"Time there was a tie of 5 sports, initiating randomizer!")
        em = discord.Embed(title="Sport for Today!", description=f"The time picked for today is - {random.choice(s)}!")
        mssge = await chn.send(f"{ping} - {str(len(bot.data['wt']['time']['reactants'].keys()))}", embed=em)
        bot.data['wt']['time']['id2'] = mssge.id
        await mssg.delete()




@msg4.before_loop
async def before_msg4():
    for _ in range(60*60*24):
        if datetime.now().hour == 18 and datetime.now().minute == 1:
            return
        await asyncio.sleep(1)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_member_ban(guild, user):
    if not hasattr(guild, 'id'):
        return
    else:
        if str(guild.id) not in bot.data['logs']:
            return
    global ban_reason
    log_chat = bot.get_channel(bot.data['logs'][str(guild.id)])
    em = discord.Embed(description=f"**Member banned**\n {user.mention}", color=discord.Color.red(), timestamp=datetime.utcnow())
    if ban_reason != "":
        em.add_field(name="Reason", value=str(ban_reason))
    em.set_author(name=user.name + "#" + user.discriminator, icon_url=user.avatar_url)
    em.set_thumbnail(url=user.avatar_url)
    await log_chat.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_message_edit(payload):  
    before = payload.cached_message
    channel = bot.get_channel(payload.channel_id)
    after = await channel.fetch_message(payload.message_id)
    if not hasattr(after.guild, 'id'):
        return
    else:
        if str(after.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(after.guild.id)])
    bc = f'{bot.CROSS_MARK} Not in Memory!'
    if hasattr(before, 'content'):
        if len(before.content) > 1024:
            before.content = before.content[0:1020] + "\n..."
        if len(after.content) > 1024:
            after.content = before.content[0:1020] + "\n..."
        bc = before.content
    if str(after.content) == "":
        return
    if after.author == bot.user:
        return
    em = discord.Embed(description=f"**Message edited in {str(channel.mention)}** - [Message]({after.jump_url})", color=discord.Color.purple(), timestamp=datetime.utcnow())
    em.add_field(name=f"**Before**", value=str(bc), inline=False)
    em.add_field(name=f"**After**", value=str(after.content), inline=False)
    em.set_author(name=str(after.author), icon_url=after.author.avatar_url)
    em.set_footer(text="MESSAGE ID: " + str(after.id))
    await log_chat.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_message_delete(payload):
    message = payload.cached_message
    if not hasattr(payload, 'guild_id'):
        return
    else:
        if str(payload.guild_id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(payload.guild_id)])  
    bc = f'{bot.CROSS_MARK} Not in Memory!'
    auth = ""
    if hasattr(message, 'content'):
        if len(message.content) > 1024:
            message.content = message.content[0:1020] + "\n..."
        if str(message.content) == "":
            return
        bc = message.content
    if hasattr(message, 'author'):
        auth =  f" - {message.author.mention}"
    channel = bot.get_channel(payload.channel_id)
    em = discord.Embed(description=f"**Message deleted in {str(channel.mention)}**\n{bc}{auth}", color=discord.Color.red(), timestamp=datetime.utcnow())
    if hasattr(message, 'author'):
        em.set_author(name=str(message.author), icon_url=message.author.avatar_url)
    if hasattr(message, 'id'):
        em.set_footer(text="MESSAGE ID: " + str(message.id))
    await log_chat.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_bulk_message_delete(payload):
    if not hasattr(payload, 'guild_id'):
        return
    else:
        if str(payload.guild_id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(payload.guild_id)])
    messages = payload.cached_messages
    message_contents = "\n".join([str(message.author.mention)+" : "+message.content for message in messages])
    channel = bot.get_channel(int(payload.channel_id))
    em = discord.Embed(description=f"**Bulk message delete in {str(channel.mention)}** \n {str(message_contents)}", color=discord.Color.red(), timestamp=datetime.utcnow())
    em.set_footer(text="CHANNEL ID: " + str(channel.id))
    await log_chat.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_member_join(member):
    if not hasattr(member.guild, 'id'):
        return
    else:
        if str(member.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(member.guild.id)])
    date_format = "%a, %d %b %Y %I:%M %p"
    em = discord.Embed(description= f"**Member Joined** - {member.mention}", color=discord.Color.green(), timestamp=datetime.utcnow())
    em.set_author(name=str(member), icon_url=member.avatar_url)
    em.add_field(name="Joined", value=member.joined_at.strftime(date_format))  
    members = sorted(member.guild.members, key=lambda m: m.joined_at)
    em.add_field(name="Join position", value=str(members.index(member)+1))
    em.add_field(name="Registered", value=member.created_at.strftime(date_format), inline=False)
    em.set_footer(text="USER ID: " + str(member.id))
    await log_chat.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_member_remove(member):
    if not hasattr(member.guild, 'id'):
        return
    else:
        if str(member.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(member.guild.id)])
    global kicks
    if kicks == True:
        kicks = False
        return
    else:
        date_format = "%a, %d %b %Y %I:%M %p"
        em = discord.Embed(description= f"**Member Left** - {member.mention}", color=discord.Color.red(), timestamp=datetime.utcnow())
        em.set_author(name=str(member), icon_url=member.avatar_url)
        em.add_field(name="Joined", value=member.joined_at.strftime(date_format), inline=False)
        em.add_field(name="Registered", value=member.created_at.strftime(date_format), inline=False)
        if len(member.roles) > 1:
            role_string = ' '.join([r.mention for r in member.roles][1:])
            em.add_field(name="Roles [{}]".format(len(member.roles)-1), value=role_string, inline=False)
        em.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_member_update(before, after):
    if not hasattr(after.guild, 'id'):
        return
    else:
        if str(after.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(after.guild.id)])
    if before.roles != after.roles:
        for role in before.roles:
            if role not in after.roles:
                em = discord.Embed(description=f"**Role removed from** {before.mention} \n**Role** - {role.mention}", color=discord.Color.red(), timestamp=datetime.utcnow())
                em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
                em.set_footer(text="USER ID: " + str(after.id)) 
                em.set_thumbnail(url=after.avatar_url)
                await log_chat.send(embed=em)
        for role in after.roles:
            if role not in before.roles:
                em = discord.Embed(description=f"**Role added to** {after.mention} \n**Role** - {role.mention}", color=discord.Color.green(), timestamp=datetime.utcnow())
                em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
                em.set_footer(text="USER ID: " + str(after.id))
                em.set_thumbnail(url=after.avatar_url)
                await log_chat.send(embed=em)

    elif before.nick != after.nick:
        if after.nick == None:
            before.nick = before.nick
            em = discord.Embed(description=f"**Nickname removed for** - {after.mention}", color=discord.Color.blue(), timestamp=datetime.utcnow())
            em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
            em.add_field(name="Before", value=f"{before.nick}")
            em.add_field(name="After", value=f"{after.nick}")
            em.set_thumbnail(url=after.avatar_url)
            em.set_footer(text="USER ID: " + str(after.id))
        if before.nick == None:
            before.nick = before.nick
            em = discord.Embed(description=f"**Nickname added for** - {after.mention}", color=discord.Color.blue(), timestamp=datetime.utcnow())
            em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
            em.add_field(name="Before", value=f"{before.nick}")
            em.add_field(name="After", value=f"{after.nick}")
            em.set_thumbnail(url=after.avatar_url)
            em.set_footer(text="USER ID: " + str(after.id))
        if after.nick != None:
            if before.nick != None:
                em = discord.Embed(description=f"**Nickname changed for** - {after.mention}", color=discord.Color.blue(), timestamp=datetime.utcnow())
                em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
                em.add_field(name="Before", value=f"{before.nick}")
                em.add_field(name="After", value=f"{after.nick}")
                em.set_thumbnail(url=after.avatar_url)
                em.set_footer(text="USER ID: " + str(after.id)) 
        await log_chat.send(embed=em)
    else:
        await save()
        return

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_invite_create(invite):
    if not hasattr(invite.guild, 'id'):
        return
    else:
        if str(invite.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(invite.guild.id)])
    em = discord.Embed(title= "New invite created", color=discord.Color.green(), timestamp=datetime.utcnow())
    em.add_field(name="Invite", value=str(invite), inline=False)
    em.add_field(name="Creater", value=str(invite.inviter.mention), inline=True)
    em.add_field(name="Channel", value=str(invite.channel.mention), inline=True)
    em.set_thumbnail(url=invite.guild.icon_url)
    em.set_footer(text="USER ID: " + str(invite.inviter.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_invite_delete(invite):
    if not hasattr(invite.guild, 'id'):
        return
    else:
        if str(invite.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(invite.guild.id)])
    em = discord.Embed(title= "Old invite revoked", color=discord.Color.red(), timestamp=datetime.utcnow())
    em.add_field(name="Invite", value=str(invite), inline=False)
    em.add_field(name="Channel", value=str(invite.channel), inline=True)
    em.set_thumbnail(url=invite.guild.icon_url)
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_channel_create(channel):
    if not hasattr(channel.guild, 'id'):
        return
    else:
        if str(channel.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(channel.guild.id)])
    em = discord.Embed(title=f"Channel Created - #{channel}", color=discord.Color.green(), timestamp=datetime.utcnow())
    em.add_field(name="Category", value=f"`{channel.category}`")
    em.set_thumbnail(url=channel.guild.icon_url)
    em.set_footer(text="CHANNEL ID: " + str(channel.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_channel_delete(channel):
    if not hasattr(channel.guild, 'id'):
        return
    else:
        if str(channel.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(channel.guild.id)])
    em = discord.Embed(title=f"Channel Deleted - #{channel}", color=discord.Color.red(), timestamp=datetime.utcnow())
    em.add_field(name="Category", value=f"`{channel.category}`")
    em.set_thumbnail(url=channel.guild.icon_url)
    em.set_footer(text="CHANNEL ID: " + str(channel.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_reaction_add(payload):
    if not hasattr(payload, 'guild_id'):
        return
    else:
        if str(payload.guild_id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(payload.guild_id)])
    emoji = payload.emoji
    member = payload.member
    channel = bot.get_channel(payload.channel_id)
    guild = channel.guild
    message = await channel.fetch_message(payload.message_id)
    if member.id == bot.user.id:
        return
    em = discord.Embed(description=f"**‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎Reaction added in {channel.mention}** - [Message]({message.jump_url})   ", color=discord.Color.green(), timestamp=datetime.utcnow())
    em.add_field(name="Emoji", value=f"{str(emoji)}", inline=False)
    em.add_field(name="Message by", value=f"{message.author.mention}", inline=True)
    em.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
    em.set_footer(text="MESSAGE ID: " + str(message.id))
    await log_chat.send(embed=em)
    if message.id == bot.data['ticket']['msg'][str(guild.id)]:
        em = discord.Embed(description=f"{member.mention} Are you sure?", timestamp=datetime.utcnow())
        mes = await channel.send(embed=em)
        await mes.add_reaction(bot.TICK_MARK)
        await mes.add_reaction(bot.CROSS_MARK)
        def check(reaction, user):
            return reaction.message.id == mes.id and str(reaction.emoji) in [bot.TICK_MARK, bot.CROSS_MARK] and user.id == member.id
        try:
            r, u = await bot.wait_for('reaction_add', timeout= 30, check=check)
            u = u
        except asyncio.TimeoutError:
            em = discord.Embed(description=f"{bot.CROSS_MARK} You ran out of time! Please re-react!", timestamp=datetime.utcnow())
            me = await channel.send(embed=em)
            await asyncio.sleep(5)
            await mes.delete()
            await me.delete()
            await message.remove_reaction(emoji, member)
            return
        if str(r.emoji) == bot.CROSS_MARK:
            em = discord.Embed(description=f"{bot.CROSS_MARK} {member.mention} Cancelling process!", timestamp=datetime.utcnow())
            memm = await channel.send(embed=em)
            await asyncio.sleep(5)
            await mes.delete()
            await memm.delete()
            await message.remove_reaction(emoji, member)
            return
        if str(r.emoji) == bot.TICK_MARK:
            em = discord.Embed(description=f"{bot.TICK_MARK} {member.mention} Creating ticket!", timestamp=datetime.utcnow())
            memm = await channel.send(embed=em)
        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
        member.bot: discord.PermissionOverwrite(read_messages=True)
        }
        if int(bot.data['ticket']['staff'][str(guild.id)]) != '':
            role = discord.utils.find(lambda m: m.id==int(bot.data['ticket']['staff'][str(guild.id)]))
            overwrites += {role: discord.PermissionOverwrite(read_messages=True)}
        chn = await guild.create_text_channel(f"#{bot.data['ticket']['count'][str(guild.id)]}-{member.name}", overwrites=overwrites)
        em = discord.Embed(title=f"Ticket #{bot.data['ticket']['count'][str(guild.id)]}", timestamp=datetime.utcnow(), category='tickets')
        em.add_field(name='Creator', value=member.mention)
        await chn.send(embed=em)
        await message.remove_reaction(emoji, member)
        bot.data['ticket']['count'][str(guild.id)] = bot.data['ticket']['count'][str(guild.id)] + 1
        await asyncio.sleep(5)
        await mes.delete()
        await memm.delete()
        bot.data['ticket']['val'][str(guild.id)][str(chn)] = member.id
    if message.id == bot.data['wt']['sport']['id']:
        if str(emoji) == '🏀':
            bot.data['wt']['sport']['votes']['bb'] = bot.data['wt']['sport']['votes']['bb'] + 1
            emj = "bb"
        if str(emoji) == '⚽':
            bot.data['wt']['sport']['votes']['fb'] = bot.data['wt']['sport']['votes']['fb'] + 1
            emj = "fb"
        if str(emoji) == '🏸':
            bot.data['wt']['sport']['votes']['bm'] = bot.data['wt']['sport']['votes']['bm'] + 1
            emj = "bm"
        if str(emoji) == '🏏':
            bot.data['wt']['sport']['votes']['cr'] = bot.data['wt']['sport']['votes']['cr'] + 1
            emj = "cr"
        if str(emoji) == '🏓':
            bot.data['wt']['sport']['votes']['tt'] = bot.data['wt']['sport']['votes']['tt'] + 1
            emj = "tt"
        if str(emoji) == bot.CROSS_MARK:
            if str(member.mention) in bot.data['wt']['sport']['reactants'] != "":
                em = bot.data['wt']['sport']['reactants'][str(member.mention)]
                bot.data['wt']['sport']['votes'][em] = bot.data['wt']['sport']['votes'][em] - 1
                del bot.data['wt']['sport']['reactants'][str(member.mention)]
            return
        if str(member.mention) in bot.data['wt']['sport']['reactants'] != "":
            em = bot.data['wt']['sport']['reactants'][str(member.mention)]
            bot.data['wt']['sport']['votes'][em] = bot.data['wt']['sport']['votes'][em] - 1


        bot.data['wt']['sport']['reactants'][str(member.mention)] = emj
    if message.id == bot.data['wt']['time']['id']:
        if str(emoji) == '🕡':
            bot.data['wt']['time']['votes']['65'] = bot.data['wt']['time']['votes']['65'] + 1
            emj = "65"
        if str(emoji) == '🕖':
            bot.data['wt']['time']['votes']['70'] = bot.data['wt']['time']['votes']['70'] + 1
            emj = "70"
        if str(emoji) == '🕢':
            bot.data['wt']['time']['votes']['75'] = bot.data['wt']['time']['votes']['75'] + 1
            emj = "75"
        if str(emoji) == '🕗':
            bot.data['wt']['time']['votes']['80'] = bot.data['wt']['time']['votes']['80'] + 1
            emj = "80"
        if str(emoji) == '🕣':
            bot.data['wt']['time']['votes']['85'] = bot.data['wt']['time']['votes']['85'] + 1
            emj = "85"
        if str(emoji) == bot.CROSS_MARK:
            if str(member.mention) in bot.data['wt']['time']['reactants'] != "":
                em = bot.data['wt']['time']['reactants'][str(member.mention)]
                bot.data['wt']['time']['votes'][em] = bot.data['wt']['time']['votes'][em] - 1
                del bot.data['wt']['time']['reactants'][str(member.mention)]
            return
        if str(member.mention) in bot.data['wt']['time']['reactants'] != "":
            em = bot.data['wt']['time']['reactants'][str(member.mention)]
            bot.data['wt']['time']['votes'][em] = bot.data['wt']['time']['votes'][em] - 1


        bot.data['wt']['time']['reactants'][str(member.mention)] = emj

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_reaction_remove(payload):
    if not hasattr(payload, 'guild_id'):
        return
    else:
        if str(payload.guild_id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(payload.guild_id)])
    emoji = payload.emoji
    user = payload.user_id
    member = bot.get_user(user)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    em = discord.Embed(description=f"**Reaction removed in {channel.mention}** - [Message]({message.jump_url})", color=discord.Color.red(), timestamp=datetime.utcnow())
    em.add_field(name="Emoji", value=f"{str(emoji)}", inline=False)
    em.add_field(name="Message by", value=f"{message.author.mention}", inline=False)
    em.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
    em.set_footer(text="MESSAGE ID: " + str(message.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_reaction_clear(payload):
    if not hasattr(payload, 'guild_id'):
        return
    else:
        if str(payload.guild_id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(payload.guild_id)])
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    em = discord.Embed(title=f"Reactions Cleared", color=discord.Color.red(), timestamp=datetime.utcnow())
    em.add_field(name="Message", value=f"[Click Here!]({message.jump_url})", inline=False)
    em.set_thumbnail(url=channel.guild.icon_url)
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_reaction_clear_emoji(payload):
    if not hasattr(payload, 'guild_id'):
        return
    else:
        if str(payload.guild_id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(payload.guild_id)])
    emoji = payload.emoji
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    em = discord.Embed(title=f"Emoji Cleared", color=discord.Color.red(), timestamp=datetime.utcnow())
    em.add_field(name="Emoji", value=f"{str(emoji)}", inline=False)
    em.add_field(name="Message", value=f"[Click Here!]({message.jump_url})", inline=False)
    em.set_thumbnail(url=channel.guild.icon_url)
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_channel_update(before, after):
    if not hasattr(after.guild, 'id'):
        return
    else:
        if str(after.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(after.guild.id)])
    valueb = ""
    valuea = ""
    em = discord.Embed(title=f'Channel "{before.name}" Updated', color=discord.Color.blue(), timestamp=datetime.utcnow())
    if before.category != after.category:
        valueb += f"**Category** - {before.category}\n"
        valuea += f"**Category** - {after.category}\n"
    if before.name != after.name:
        valueb += f"**Name** - {before.name}\n"
        valuea += f"**Name** - {after.name}\n"
    if before.permissions_synced != after.permissions_synced:
        if before.permissions_synced == False:
            valueb += "None\n"
            valuea += f"**Synced with** {after.category}\n"
        if before.permissions_synced == True:
            valueb += "None\n"
            valuea += f"**Unsynced with** {after.category}\n"
    if before.changed_roles != after.changed_roles:
        if len(before.changed_roles) < len(after.changed_roles):
            for role in after.changed_roles:
                if role not in before.changed_roles: 
                    valueb += "None\n"
                    valuea += f"**Overwrite added - ** {role.mention}\n"
        if len(before.changed_roles) > len(after.changed_roles):
            for role in before.changed_roles:
                if role not in after.changed_roles: 
                    valueb += "None\n"
                    valuea += f"**Overwrite removed - ** {role.mention}\n"
    if before.topic != after.topic:
        if before.topic == "":
            valueb += "None\n"
            valuea += f"**Topic added - ** {after.mention}\n"
        if after.topic == "":
            valueb += "None\n"
            valuea += f"**Topic removed - ** {role.mention}\n"
    em.add_field(name="Before", value=valueb)
    em.add_field(name="After", value=valuea)
    em.set_thumbnail(url=before.guild.icon_url)
    em.set_footer(text="ROLE ID: " + str(before.id))
    if valuea != "" and valueb != "":
        await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_channel_pins_update(channel, last_pin):
    if not hasattr(channel.guild, 'id'):
        return
    else:
        if str(channel.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(channel.guild.id)])
    status = "Pins Updated"
    pins = await channel.pins()
    pin = "\n".join(["[Click Here!](" + pin.jump_url + ")" for pin in pins])
    if pin == "":
        pin = None
        status = "Pins Removed"
    em = discord.Embed(title=status, color=discord.Color.blue(), timestamp=datetime.utcnow())
    em.add_field(name="Channel", value=channel.mention)
    em.add_field(name="Pins", value=str(pin))
    em.set_thumbnail(url=channel.guild.icon_url)
    em.set_footer(text="CHANNEL ID: " + str(channel.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_update(before, after):
    if not hasattr(after, 'id'):
        return
    else:
        if str(after.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(after.guild.id)])
    if before.banner != after.banner:
        emold = discord.Embed(title=f"{after.name}'s' Banner Changed", description="Before", color=discord.Color.blue(), timestamp=datetime.utcnow())
        emold.set_image(url=before.banner_url)
        emold.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emold)
        emnew = discord.Embed(title=f"{after.name}'s Banner Changed", description="After", color=discord.Color.blue(), timestamp=datetime.utcnow())
        emnew.set_image(url=after.banner_url)
        emnew.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emnew)
    if before.name != after.name:
        em = discord.Embed(title="Server Name Changed", color=discord.Color.blue(), timestamp=datetime.utcnow())
        em.add_field(name="Before", value=before.name, inline=False)
        em.add_field(name="After", value=after.name, inline=False)
        em.set_thumbnail(url=before.icon_url)
        em.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=em)
    if before.icon != after.icon:
        emold = discord.Embed(title=f"{after.name}'s Icon Changed", description="Before", color=discord.Color.blue(), timestamp=datetime.utcnow())
        emold.set_image(url=before.icon_url)
        emold.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emold)
        emnew = discord.Embed(title=f"{after.name}'s Icon Changed", description="After", color=discord.Color.blue(), timestamp=datetime.utcnow())
        emnew.set_image(url=after.icon_url)
        emnew.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emnew)
    if before.owner != after.owner:
        em = discord.Embed(title="Server Owner Changed", color=discord.Color.blue(), timestamp=datetime.utcnow())
        em.add_field(name="Before", value=before.owner.mention, inline=False)
        em.add_field(name="After", value=after.owner.mention, inline=False)
        em.set_thumbnail(url=before.icon_url)
        em.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=em)
    if before.splash != after.splash:
        emold = discord.Embed(title=f"{after.name}'s' Splash Changed", description="Before", color=discord.Color.blue(), timestamp=datetime.utcnow())
        emold.set_image(url=before.spash_url)
        emold.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emold)
        emnew = discord.Embed(title=f"{after.name}'s Splash Changed", description="After", color=discord.Color.blue(), timestamp=datetime.utcnow())
        emnew.set_image(url=after.spash_url)
        emnew.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emnew)
    if before.premium_subscription_count != after.premium_subscription_count:
        if before.premium_subscription_count > after.premium_subscription_count:
            em = discord.Embed(title=f"{after.name} lost boosts", color=discord.Color.red(), timestamp=datetime.utcnow())
            em.add_field(name="Before", value=before.premium_subscription_count, inline=False)
            em.add_field(name="After", value=after.premium_subscription_count, inline=False)
            await log_chat.send(embed=em)
        else:
            em = discord.Embed(title=f"{after.name} gained boosts", color=discord.Color.green(), timestamp=datetime.utcnow())
            em.add_field(name="Before", value=before.premium_subscription_count, inline=False)
            em.add_field(name="After", value=after.premium_subscription_count, inline=False)
            await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_role_create(role):
    if not hasattr(role.guild, 'id'):
        return
    else:
        if str(role.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(role.guild.id)])
    em = discord.Embed(title=f'Role "{role.name}" Created', color=discord.Color.green(), timestamp=datetime.utcnow())
    em.set_thumbnail(url=role.guild.icon_url)
    em.set_footer(text="ROLE ID: " + str(role.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_role_delete(role):
    if not hasattr(role.guild, 'id'):
        return
    else:
        if str(role.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(role.guild.id)])
    em = discord.Embed(title=f'Role "{role.name}" Deleted', color=discord.Color.red(), timestamp=datetime.utcnow())
    em.set_thumbnail(url=role.guild.icon_url)
    em.set_footer(text="ROLE ID: " + str(role.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_role_update(before, after):
    if not hasattr(after.guild, 'id'):
        return
    else:
        if str(after.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(after.guild.id)])
    valueb = ""
    valuea = ""
    permissions = ""
    emoji = ""
    em = discord.Embed(title=f'Role "{before.name}" Updated', color=discord.Color.blue(), timestamp=datetime.utcnow())
    if before.name != after.name:
        valueb += f"**Name** - {before.name}\n"
        valuea += f"**Name** - {after.name}\n"
    if before.color != after.color:
        valueb += f"**Color** - {str(before.color)}\n"
        valuea += f"**Color** - {str(after.color)}\n"
    if before.permissions.add_reactions != after.permissions.add_reactions:
        if after.permissions.add_reactions == True:
            emoji = bot.TICK_MARK
        if after.permissions.add_reactions == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**add_reactions** `{after.permissions.add_reactions}`\n"
    if before.permissions.administrator != after.permissions.administrator:
        if after.permissions.administrator == True:
            emoji = bot.TICK_MARK
        if after.permissions.administrator == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**administrator** `{after.permissions.administrator}`\n"
    if before.permissions.attach_files != after.permissions.attach_files:
        if after.permissions.attach_files == True:
            emoji = bot.TICK_MARK
        if after.permissions.attach_files == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**attach_files** `{after.permissions.attach_files}`\n"
    if before.permissions.ban_members != after.permissions.ban_members:
        if after.permissions.ban_members == True:
            emoji = bot.TICK_MARK
        if after.permissions.ban_members == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**ban_members** `{after.permissions.ban_members}`\n"
    if before.permissions.change_nickname != after.permissions.change_nickname:
        if after.permissions.change_nickname == True:
            emoji = bot.TICK_MARK
        if after.permissions.change_nickname == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**change_nickname** `{after.permissions.change_nickname}`\n"
    if before.permissions.connect != after.permissions.connect:
        if after.permissions.connect == True:
            emoji = bot.TICK_MARK
        if after.permissions.connect == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**connect** `{after.permissions.connect}`\n"
    if before.permissions.create_instant_invite != after.permissions.create_instant_invite:
        if after.permissions.create_instant_invite == True:
            emoji = bot.TICK_MARK
        if after.permissions.create_instant_invite == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**create_instant_invite** `{after.permissions.create_instant_invite}`\n"
    if before.permissions.deafen_members != after.permissions.deafen_members:
        if after.permissions.deafen_members == True:
            emoji = bot.TICK_MARK
        if after.permissions.deafen_members == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**deafen_members** `{after.permissions.deafen_members}`\n"
    if before.permissions.embed_links != after.permissions.embed_links:
        if after.permissions.embed_links == True:
            emoji = bot.TICK_MARK
        if after.permissions.embed_links == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**embed_links** `{after.permissions.embed_links}`\n"
    if before.permissions.external_emojis != after.permissions.external_emojis:
        if after.permissions.external_emojis == True:
            emoji = bot.TICK_MARK
        if after.permissions.external_emojis == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**external_emojis** `{after.permissions.external_emojis}`\n"
    if before.permissions.kick_members != after.permissions.kick_members:
        if after.permissions.kick_members == True:
            emoji = bot.TICK_MARK
        if after.permissions.kick_members == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**kick_members** `{after.permissions.kick_members}`\n"
    if before.permissions.manage_channels != after.permissions.manage_channels:
        if after.permissions.manage_channels == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_channels == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_channels** `{after.permissions.manage_channels}`\n"
    if before.permissions.manage_emojis != after.permissions.manage_emojis:
        if after.permissions.manage_emojis == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_emojis == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_emojis** `{after.permissions.manage_emojis}`\n"
    if before.permissions.manage_guild != after.permissions.manage_guild:
        if after.permissions.manage_guild == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_guild == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_guild** `{after.permissions.manage_guild}`\n"
    if before.permissions.manage_messages != after.permissions.manage_messages:
        if after.permissions.manage_messages == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_messages == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_messages** `{after.permissions.manage_messages}`\n"
    if before.permissions.manage_nicknames != after.permissions.manage_nicknames:
        if after.permissions.manage_nicknames == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_nicknames == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_nicknames** `{after.permissions.manage_nicknames}`\n"
    if before.permissions.manage_permissions != after.permissions.manage_permissions:
        if after.permissions.manage_permissions == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_permissions == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_permissions** `{after.permissions.manage_permissions}`\n"
    if before.permissions.manage_roles != after.permissions.manage_roles:
        if after.permissions.manage_roles == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_roles == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_roles** `{after.permissions.manage_roles}`\n"
    if before.permissions.manage_webhooks != after.permissions.manage_webhooks:
        if after.permissions.manage_webhooks == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_webhooks == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_webhooks** `{after.permissions.manage_webhooks}`\n"
    if before.permissions.mention_everyone != after.permissions.mention_everyone:
        if after.permissions.mention_everyone == True:
            emoji = bot.TICK_MARK
        if after.permissions.mention_everyone == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**mention_everyone** `{after.permissions.mention_everyone}`\n"
    if before.permissions.move_members != after.permissions.move_members:
        if after.permissions.move_members == True:
            emoji = bot.TICK_MARK
        if after.permissions.move_members == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**move_members** `{after.permissions.move_members}`\n"
    if before.permissions.mute_members != after.permissions.mute_members:
        if after.permissions.mute_members == True:
            emoji = bot.TICK_MARK
        if after.permissions.mute_members == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**mute_members** `{after.permissions.mute_members}`\n"
    if before.permissions.priority_speaker != after.permissions.priority_speaker:
        if after.permissions.priority_speaker == True:
            emoji = bot.TICK_MARK
        if after.permissions.priority_speaker == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**priority_speaker** `{after.permissions.priority_speaker}`\n"
    if before.permissions.read_message_history != after.permissions.read_message_history:
        if after.permissions.read_message_history == True:
            emoji = bot.TICK_MARK
        if after.permissions.read_message_history == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**read_message_history** `{after.permissions.read_message_history}`\n"
    if before.permissions.read_messages != after.permissions.read_messages:
        if after.permissions.read_messages == True:
            emoji = bot.TICK_MARK
        if after.permissions.read_messages == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**read_messages** `{after.permissions.read_messages}`\n"
    if before.permissions.send_messages != after.permissions.send_messages:
        if after.permissions.send_messages == True:
            emoji = bot.TICK_MARK
        if after.permissions.send_messages == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**send_messages** `{after.permissions.send_messages}`\n"
    if before.permissions.send_tts_messages != after.permissions.send_tts_messages:
        if after.permissions.send_tts_messages == True:
            emoji = bot.TICK_MARK
        if after.permissions.send_tts_messages == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**send_tts_messages** `{after.permissions.send_tts_messages}`\n"
    if before.permissions.speak != after.permissions.speak:
        if after.permissions.speak == True:
            emoji = bot.TICK_MARK
        if after.permissions.speak == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**speak** `{after.permissions.speak}`\n"
    if before.permissions.stream != after.permissions.stream:
        if after.permissions.stream == True:
            emoji = bot.TICK_MARK
        if after.permissions.stream == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**stream** `{after.permissions.stream}`\n"
    if before.permissions.use_external_emojis != after.permissions.use_external_emojis:
        if after.permissions.use_external_emojis == True:
            emoji = bot.TICK_MARK
        if after.permissions.use_external_emojis == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**use_external_emojis** `{after.permissions.use_external_emojis}`\n"
    if before.permissions.use_voice_activation != after.permissions.use_voice_activation:
        if after.permissions.use_voice_activation == True:
            emoji = bot.TICK_MARK
        if after.permissions.use_voice_activation == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**use_voice_activation** `{after.permissions.use_voice_activation}`\n"
    if before.permissions.view_audit_log != after.permissions.view_audit_log:
        if after.permissions.view_audit_log == True:
            emoji = bot.TICK_MARK
        if after.permissions.view_audit_log == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**view_audit_log** `{after.permissions.view_audit_log}`\n"
    if before.permissions.view_guild_insights != after.permissions.view_guild_insights:
        if after.permissions.view_guild_insights == True:
            emoji = bot.TICK_MARK
        if after.permissions.view_guild_insights == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**view_guild_insights** `{after.permissions.view_guild_insights}`\n"
    if before.hoist != after.hoist:
        if after.hoist == True:
            emoji = bot.TICK_MARK
        if after.hoist == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**display_seperately** `{after.hoist}`\n"
    if before.mentionable != after.mentionable:
        if after.mentionable == True:
            emoji = bot.TICK_MARK
        if after.mentionable == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**mentionable** `{after.mentionable}`\n"
    if valuea == "":
        valuea = None
    if valueb == "":
        valueb = None
    em.add_field(name="Before", value=valueb)
    em.add_field(name="After", value=valuea)
    if permissions != "":
        em.add_field(name="Permissions", value=permissions)
    em.set_thumbnail(url=before.guild.icon_url)
    em.set_footer(text="ROLE ID: " + str(before.id))
    if valuea != None or valueb != None or permissions != '':
        await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_voice_state_update(member, before, after):
    if not hasattr(member.guild, 'id'):
        return
    else:
        if str(member.guild.id) not in bot.data['logs']:
            return
    log_chat = bot.get_channel(bot.data['logs'][str(member.guild.id)])
    status = ""
    status2 = ""
    status3 = ""
    status4 = ""
    status5 = ""
    status6 = ""
    status7 = ""
    status8 = ""
    field_2 = False
    color = ""
    color2 = ""
    color3 = ""
    color4 = ""
    color5 = ""
    color6 = ""
    color7 = ""
    color8 = ""
    if before.channel != after.channel:
        if before.channel == None:
            status = "**Member joined voice channel**"
            color = discord.Color.green()
        if after.channel == None:
            status = "**Member left voice channel**"
            color = discord.Color.red()
        if before.channel != None and after.channel != None:
            status = "**Member changed voice channels**"
            field_2 = True
            color = discord.Color.blue()
        em = discord.Embed(description=f"{status} - {member.mention}", color=color, timestamp=datetime.utcnow())
        em.set_author(name=member, icon_url=member.avatar_url)
        if field_2 == True:
            em.add_field(name="Channel 1", value=before.channel)
            em.add_field(name="Channel 2", value=after.channel)
        else:
            if after.channel == None:
                em.add_field(name="Channel", value=before.channel)
            else:
                em.add_field(name="Channel", value=after.channel)
        em.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em)
    if before.mute != after.mute:
        if before.mute == False:
            status2 = "**Member muted**"
            color2 = discord.Color.red()
        if after.mute == False:
            status2 = "**Member unmuted**"
            color2 = discord.Color.green()
        em2 = discord.Embed(description=f"{status2} - {member.mention}", color=color2, timestamp=datetime.utcnow())
        em2.set_author(name=member, icon_url=member.avatar_url)
        em2.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em2)
    if before.deaf != after.deaf:
        if before.deaf == False:
            status3 = "**Member deafened**"
            color3 = discord.Color.red()
        if after.deaf == False:
            status3 = "**Member undefeaned**"
            color3 = discord.Color.green()
        em3 = discord.Embed(description=f"{status3} - {member.mention}", color=color3, timestamp=datetime.utcnow())
        em3.set_author(name=member, icon_url=member.avatar_url)
        em3.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em3)
    if before.self_mute != after.self_mute:
        if before.self_mute == False:
            status4 = "**Member self muted**"
            color4 = discord.Color.red()
        if after.self_mute == False:
            status4 = "**Member self unmuted**"
            color4 = discord.Color.green()
        em4 = discord.Embed(description=f"{status4} - {member.mention}", color=color4, timestamp=datetime.utcnow())
        em4.set_author(name=member, icon_url=member.avatar_url)
        em4.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em4)
    if before.self_deaf != after.self_deaf:
        if before.self_deaf == False:
            status5 = "**Member self deafened**"
            color5 = discord.Color.red()
        if after.self_deaf == False:
            status5 = "**Member self undefeaned**"
            color5 = discord.Color.green()
        em5 = discord.Embed(description=f"{status5} - {member.mention}", color=color5, timestamp=datetime.utcnow())
        em5.set_author(name=member, icon_url=member.avatar_url)
        em5.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em5)
    if before.self_stream != after.self_stream:
        if before.self_stream == False:
            status6 = "**Member started streaming**"
            color6 = discord.Color.green()
        if after.self_stream == False:
            status6 = "**Member stopped streaming**"
            color6 = discord.Color.red()
        em6 = discord.Embed(description=f"{status6} - {member.mention}", color=color6, timestamp=datetime.utcnow())
        em6.set_author(name=member, icon_url=member.avatar_url)
        em6.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em6)
    if before.self_video != after.self_video:
        if before.self_video == False:
            status7 = "**Member started sharing their video**"
            color7 = discord.Color.green()
        if after.self_video == False:
            status7 = "**Member stopped sharing their video**"
            color7 = discord.Color.red()
        em7 = discord.Embed(description=f"{status7} - {member.mention}", color=color7, timestamp=datetime.utcnow())
        em7.set_author(name=member, icon_url=member.avatar_url)
        em7.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em7)
    if before.self_video != after.self_video:
        if before.afk == False:
            status8 = "**Member now afk**"
            color8 = discord.Color.red()
        if after.afk == False:
            status8 = "**Member not afk**"
            color8 = discord.Color.green()
        em8 = discord.Embed(description=f"{status8} - {member.mention}", color=color8, timestamp=datetime.utcnow())
        em8.set_author(name=member, icon_url=member.avatar_url)
        em8.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em8)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_user_update(before, after):
    for guild in bot.data['logs']:
        if bot.data['logs'][str(guild)] != "":
            guild = int(guild)
            guildd = bot.get_guild(guild)
            if guildd.get_member(after.id) is not None:
                log_chat = bot.get_channel(bot.data['logs'][str(guild.id)])
                if before.avatar != after.avatar:
                    emold = discord.Embed(title=f"{before.display_name}'s Avatar Updated", description=f"[Before]({before.avatar_url})", color=discord.Color.blue(), timestamp=datetime.utcnow())
                    avb = before.avatar_url_as(size=512)
                    emold.set_image(url=avb)
                    emold.set_footer(text="USER ID: " + str(before.id))
                    await log_chat.send(embed=emold)
                    await asyncio.sleep(2)
                    emnew = discord.Embed(title=f"{before.display_name}'s Avatar Updated", description=f"[After]({after.avatar_url})", color=discord.Color.blue(), timestamp=datetime.utcnow())
                    ava = after.avatar_url_as(size=512)
                    emnew.set_image(url=ava)
                    emnew.set_footer(text="USER ID: " + str(before.id))
                    await log_chat.send(embed=emnew)
                else:
                    em = discord.Embed(title=f"{before.display_name}'s Name/Discriminator Updated", color=discord.Color.blue(), timestamp=datetime.utcnow())
                    em.add_field(name="Before", value=f"`{before.name}#{before.discriminator}`", inline=False)
                    em.add_field(name="After", value=f"`{after.name}#{after.discriminator}`", inline=False)
                    em.set_footer(text="USER ID: " + str(before.id))
                    em.set_thumbnail(url=before.avatar_url)
                    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_join(guild):
    bot.data['logs'][str(guild.id)] = ""

    bot.data['widt'][str(guild.id)] = ""

    bot.data['suggest']['chn'][str(guild.id)] = ""
    bot.data['suggest']['count'][str(guild.id)] = 1
    bot.data['suggest']['val'][str(guild.id)] = {}

    bot.data['ticket']['chn'][str(guild.id)] = ""
    bot.data['ticket']['count'][str(guild.id)] = 1
    bot.data['ticket']['val'][str(guild.id)] = {}
    bot.data['ticket']['staff'][str(guild.id)] = ""
    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f"cogs.{file[:-3]}")




bot.run('ODExMjQzMjQwODM2ODI1MDk5.YCvXJA.koWM9mPBTB5iwhKmCwPS1KHu0H0')
