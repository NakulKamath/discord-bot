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
@commands.has_permissions(manage_roles=True)
async def mute(ctx, mem: discord.Member=None, s: str=None):
    if mem == None:
        em = discord.Embed(description=f"{bot.CROSS_MARK} Please mention a member to mute!")
        await ctx.send(embed=em)
        return
    try:
        role = ctx.guild.get_role(bot.data['mute'][str(ctx.guild.id)])
    except:
        em = discord.Embed(description=f"{bot.CROSS_MARK} This server does not have a mute role set up! \nReply yes to automatically create one!")
        await ctx.send(embed=em)
        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.channel
        try:
            msg = await bot.wait_for('message', timeout= 30, check=check)
        except asyncio.TimeoutError:
            em = discord.Embed(description=f"{bot.CROSS_MARK} You ran out of time! Please re-type the command!")
            await ctx.channel.send(embed=em)
            return
        if msg.content.upper() == 'YES':
            role = await ctx.guild.create_role(name='muted')
            bot.data['mute'][str(ctx.guild.id)] = role.id
            for chn in ctx.guild.channels:
                await chn.set_permissions(role, read_messages=True, send_messages=False)
        return
    else:
        val = 0
        t = re.compile(r"([0-9][0-9](s|m|h|d|w))|([0-9](s|m|h|d|w))")
        if s != None:
            tts = t.match(s)
            if tts == None:
                embed = discord.Embed(description="<:cross_mark:814801897138815026> Use the syntax `XXs/m/h/d/w`!")
                await ctx.send(embed=embed)
                return
            ts = tts.group()
            if ts[-1] == 's':
                ts = ts[:-1]
                val = val + int(ts)*1000
            if ts[-1] == 'm':
                ts = ts[:-1]
                val = val + int(ts)*60000
            if ts[-1] == 'h':
                ts = ts[:-1]
                val = val + int(ts)*3600000
            if ts[-1] == 'd':
                ts = ts[:-1]
                val = val + int(ts)*86400000
            if ts[-1] == 'w':
                ts = ts[:-1]
                val = val + int(ts)*604800000
            val = round(val//1000)
            m, s = divmod(val, 60)
            h, m = divmod(m, 60)
            d, h = divmod(h, 24)
            w, d = divmod(d, 7)
            if int(w) == 0 and int(d) == 0 and int(h) == 0 and int(m) == 0 and s != 0:
                embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Muted {mem.mention} for {s}s!", timestamp=datetime.utcnow())
                await ctx.send(embed=embed)
            elif int(w) == 0 and int(d) == 0 and int(h) == 0 and int(m) != 0:
                embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Muted {mem.mention} for {m}m {s}s!", timestamp=datetime.utcnow())
                await ctx.send(embed=embed)
            elif int(w) == 0 and int(d) == 0 and int(h) != 0:
                embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Muted {mem.mention} for {h}h {m}m {s}s!", timestamp=datetime.utcnow())
                await ctx.send(embed=embed)
            elif int(w) == 0 and int(d) != 0:
                embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Muted {mem.mention} for {d}d {h}h {m}m {s}s!", timestamp=datetime.utcnow())
                await ctx.send(embed=embed)
            elif int(w) != 0:
                embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Muted {mem.mention} for {w}w {d}d {h}h {m}m {s}s!", timestamp=datetime.utcnow())
                await ctx.send(embed=embed)
            role = ctx.guild.get_role(bot.data['mute'][str(ctx.guild.id)])
            await mem.add_roles(role)
            await asyncio.sleep(val)
            await mem.remove_roles(role)
        else:
            embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Muted {mem.mention} indefinitely", timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            role = ctx.guild.get_role(bot.data['mute'][str(ctx.guild.id)])
            await mem.add_roles(role)
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
    if isinstance(error, commands.CommandOnCooldown, ):
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
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f"cogs.{file[:-3]}")



bot.run('ODExMjQzMjQwODM2ODI1MDk5.YCvXJA.koWM9mPBTB5iwhKmCwPS1KHu0H0')
