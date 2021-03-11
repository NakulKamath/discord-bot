import discord
from discord.ext import commands
import re

client = commands.Bot(command_prefix="$", intents=discord.Intents.all(), case_insensitive=True)

reaction_title = ""
description = ""
reactions = {}
reaction_message_id = ""
log = "814816975183151104"
ban_reason = ""
kicks = False
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(name="whoami")
async def whoami(context):
    channel = context.message.channel
    author = context.message.author
    await channel.send("Hi, you are " + str(author.mention) + " and you are talking to **The Oracle** a bot made for **The Matrix**!! You are currently in the channel : " + str(channel.mention))
    await context.message.author.send("You can not let the other members on the server know about this... Its top secret stuff - you are an amazing person!! : )")

@client.command(name="ONION")
async def onion(context):
    await context.send("https://cdn.discordapp.com/attachments/774156001993162793/814833307836481576/images.png")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(name="kick", pass_context = True)
async def kick(context, member: discord.Member, *, reason=None):
    global log
    global kicks
    kicks = True
    for_reason = "For reason - "
    log_chat = client.get_channel(int(log))
    if reason == None:
        reason = "No reason provided! by moderator " + str(context.message.author)
    if reason != "No reason provided! by moderator " + str(context.message.author):
        reason = reason + "! by moderator " + str(context.message.author)
    if context.message.author != member:
        if kicks == True:
            await member.kick(reason=reason)
            emk = discord.Embed(description=f"**Member kicked**\n {member.mention}", color=discord.Color.red())
            emk.add_field(name="Reason", value=reason)
            emk.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
            emk.set_thumbnail(url=member.avatar_url)
        await log_chat.send(embed=emk)
        if reason == "No reason provided! by moderator " + str(context.message.author):
            for_reason = ""
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Succesfully Kicked {member.mention} \n{for_reason} {str(reason)}")
        await context.send(embed=em)
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> You cannot kick yourself!")
        await context.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(name="ban", pass_context = True)
@commands.has_permissions(ban_members=True)
async def ban(context, member: discord.User, *, reason=None):
    global ban_reason
    for_reason = "For reason - "
    if reason == None:
        reason = "No reason provided! by moderator " + str(context.message.author)
    if reason != "No reason provided! by moderator " + str(context.message.author):
        reason = reason + "! by moderator " + str(context.message.author)
    ban_reason = str(reason)
    if context.message.author != member:
        await member.ban(reason=reason)
        if reason == "No reason provided! by moderator " + str(context.message.author):
            for_reason = ""
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Succesfully Banned {member.mention} \n{for_reason}{str(reason)}")
        await context.send(embed=em)
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> You cannot ban yourself!")
        await context.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=['ui', 'info', 'i'])
async def userinfo(context, *, user: discord.Member = None):
    if isinstance(context.channel, discord.DMChannel):
        return    
    if user is None:
        user = context.author
    date_format = "%a, %d %b %Y %I:%M %p"
    em = discord.Embed(title=str(user.display_name) + "'s User Information", color=discord.Color.blue(), description=user.mention)
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
    return await context.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=['si', 'gi', 'guildinfo'])
async def serverinfo(context):
    name = str(context.guild.name)
    owner = str(context.guild.owner)
    id = str(context.guild.id)
    memberCount = str(context.guild.member_count)
    roleCount = str(len(context.guild.roles))
    channelCount = str(len(context.guild.channels))
    textCount = str(len(context.guild.text_channels))
    voiceCount = str(len(context.guild.voice_channels))
    icon = str(context.guild.icon_url)  
    em = discord.Embed(title=name + " Server Information",color=discord.Color.blue())
    em.set_thumbnail(url=icon)
    em.add_field(name="Owner", value=owner, inline=True)
    em.add_field(name="Level", value=f"{context.guild.premium_tier} ({context.guild.premium_subscription_count}/30)", inline=True)
    em.add_field(name="The Oracle", value="<:tick_mark:814801884358901770> True", inline=True)
    em.add_field(name="Member Count", value=memberCount, inline=True)
    em.add_field(name="Role Count", value=roleCount, inline=True)
    em.add_field(name="Channel Count", value=f"{channelCount} (<:text:812696450684551199>{textCount}, <:voice:812696440114774096>{voiceCount})", inline=True)
    em.add_field(name="Rules", value=f"{context.guild.rules_channel.mention}", inline=True)
    em.add_field(name="Moderation", value=f"[Click here!](https://discord.com/channels/297301054930944011/745958042486702123/812302504330526741)", inline=True)
    em.add_field(name="Leveling", value=f"[Click here!](https://discord.com/channels/297301054930944011/745958042486702123/747274838900736040)", inline=True)
    em.set_image(url=context.guild.banner_url)
    em.set_footer(text="Server ID : " + id)
    await context.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=["ci", "channeli", "cinfo"])
async def channelinfo(context, *, channel: discord.TextChannel=None):
    date_format = "%a, %d %b %Y %I:%M %p"
    roles = ""
    if channel == None:
        channel = context.channel
    if isinstance(context.channel, discord.DMChannel):
        return
    em = discord.Embed(title=channel.name + " Channel Information", color=discord.Color.blue())
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
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=["ri", "rolei", "rinfo"])
async def roleinfo(context, *, role: discord.Role=None):
    tagss = role.tags
    date_format = "%a, %d %b %Y %I:%M %p"
    if role == None:
        eme = discord.Embed(description=f"<:cross_mark:814801897138815026> You must provide a role for this command!")
        await context.send(embed=eme)
    else:
        em = discord.Embed(title=role.name + " Role Information", color=discord.Color.blue())
        em.add_field(name="Color", value=str(role.color))
        em.add_field(name="Created at", value=str(role.created_at.strftime(date_format)))
        em.add_field(name="Position", value=str(role.position))
        em.add_field(name="Members", value=str(len(role.members)))
        em.add_field(name="Displayed", value=str(role.hoist))
        if hasattr(tagss, 'is_premium_subscriber') == True and hasattr(tagss, 'is_bot_managed') == True:
                em.add_field(name="Boost role/Bot role", value=str(role.tags.is_premium_subscriber()) + "/" + str(role.tags.is_bot_managed()))
        em.set_thumbnail(url=context.guild.icon_url)
    await context.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command()
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
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=["a", "av"])
async def avatar(context, member: discord.Member=None):
    if member == None:
        member = context.message.author 
    em = discord.Embed(title="Avatar", color=discord.Color.blue())
    em.set_image(url=member.avatar_url)
    em.set_author(name=str(member), icon_url=member.avatar_url)
    em.set_footer(text="USER ID: " + str(member.id))
    await context.channel.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=["servericon"])
async def icon(context):
    em = discord.Embed(title="Icon", color=discord.Color.blue())
    em.set_image(url=context.guild.icon_url)
    em.set_author(name=str(context.message.author), icon_url=context.message.author.avatar_url)
    em.set_footer(text="SERVER ID: " + str(context.guild.id))
    await context.channel.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=["serverbanner"])
async def banner(context):
    em = discord.Embed(title="Banner", color=discord.Color.blue())
    em.set_image(url=context.guild.banner_url)
    em.set_author(name=str(context.message.author), icon_url=context.message.author.avatar_url)
    em.set_footer(text="SERVER ID: " + str(context.guild.id))
    await context.channel.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=["owo"])
async def owofy(context, message: discord.Message=None):
    if message == None:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> You must provide text!")
        await context.send(embed=em)
    l = "l"
    ln = "w"
    r = "r"
    rn = "w"
    na = "na"
    nan = "nya"
    msg = str(message)
    if l in message:
        msg.replace(l, ln)
    if r in message:
        msg.replace(r, rn)
    if na in message:
        msg.replace(na, nan)
    await context.channel.send(msg)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_ready():
    gen_chat = client.get_channel(int(log))
    await gen_chat.send("ARB is online (don't $banall MORF)")
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("with the lives of RAIDERS"))
    print('Bot is now online!')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_ban(guild, user):
    global ban_reason
    global log
    log_chat = client.get_channel(int(log))
    em = discord.Embed(description=f"**Member banned**\n {user.mention}", color=discord.Color.red())
    if ban_reason != "":
        em.add_field(name="Reason", value=str(ban_reason))
    em.set_author(name=user.name + "#" + user.discriminator, icon_url=user.avatar_url)
    em.set_thumbnail(url=user.avatar_url)
    await log_chat.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_raw_message_edit(payload):  
    before = payload.cached_message
    channel = client.get_channel(payload.channel_id)
    after = await channel.fetch_message(payload.message_id)
    if len(before.content) > 1024:
        before.content = before.content[0:1020] + "\n..."
    if len(after.content) > 1024:
        after.content = before.content[0:1020] + "\n..."
    global log
    if str(after.content) == "":
        return
    log_chat = client.get_channel(int(log))
    if after.author == client.user:
        return
    if before == None:
        before = "Uncashed message : ("
    em = discord.Embed(description=f"**Message edited in {str(channel.mention)}** - [Message]({after.jump_url})", color=discord.Color.purple())
    em.add_field(name=f"**Before**", value=str(before.content), inline=False)
    em.add_field(name=f"**After**", value=str(after.content), inline=False)
    em.set_author(name=str(after.author), icon_url=after.author.avatar_url)
    em.set_footer(text="MESSAGE ID: " + str(after.id))
    await log_chat.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_raw_message_delete(payload):
    message = payload.cached_message
    global log
    log_chat = client.get_channel(int(log))  
    if str(message.content) == "":
        return
    channel = message.channel
    em = discord.Embed(description=f"**Message deleted in {str(channel.mention)}**\n{str(message.content)} - {message.author.mention}", color=discord.Color.red())
    em.set_author(name=str(message.author), icon_url=message.author.avatar_url)
    em.set_footer(text="MESSAGE ID: " + str(message.id))
    await log_chat.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_raw_bulk_message_delete(payload):
    messages = payload.cached_messages
    message_contents = "\n".join([str(message.author.mention)+" : "+message.content for message in messages])
    global log
    log_chat = client.get_channel(int(log))
    channel = client.get_channel(int(payload.channel_id))
    em = discord.Embed(description=f"**Bulk message delete in {str(channel.mention)}** \n {str(message_contents)}", color=discord.Color.red())
    em.set_footer(text="CHANNEL ID: " + str(channel.id))
    await log_chat.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_join(member):
    global log
    log_chat = client.get_channel(int(log))
    date_format = "%a, %d %b %Y %I:%M %p"
    em = discord.Embed(description= f"**Member Joined** - {member.mention}", color=discord.Color.green())
    em.set_author(name=str(member), icon_url=member.avatar_url)
    em.add_field(name="Joined", value=member.joined_at.strftime(date_format))  
    members = sorted(member.guild.members, key=lambda m: m.joined_at)
    em.add_field(name="Join position", value=str(members.index(member)+1))
    em.add_field(name="Registered", value=member.created_at.strftime(date_format), inline=False)
    em.set_footer(text="USER ID: " + str(member.id))
    await log_chat.send(embed=em)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_remove(member):
    global kicks
    if kicks == True:
        kicks = False
        return
    else:
        global log
        log_chat = client.get_channel(int(log))
        date_format = "%a, %d %b %Y %I:%M %p"
        em = discord.Embed(description= f"**Member Left** - {member.mention}", color=discord.Color.red())
        em.set_author(name=str(member), icon_url=member.avatar_url)
        em.add_field(name="Joined", value=member.joined_at.strftime(date_format), inline=False)
        em.add_field(name="Registered", value=member.created_at.strftime(date_format), inline=False)
        if len(member.roles) > 1:
            role_string = ' '.join([r.mention for r in member.roles][1:])
            em.add_field(name="Roles [{}]".format(len(member.roles)-1), value=role_string, inline=False)
        em.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_update(before, after):
    global log
    log_chat = client.get_channel(int(log))
    if before.roles != after.roles:
        for role in before.roles:
            if role not in after.roles:
                em = discord.Embed(description=f"**Role removed from** {before.mention} \n**Role** - {role.mention}", color=discord.Color.red())
                em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
                em.set_footer(text="USER ID: " + str(after.id)) 
                em.set_thumbnail(url=after.avatar_url)
                await log_chat.send(embed=em)
        for role in after.roles:
            if role not in before.roles:
                em = discord.Embed(description=f"**Role added to** {after.mention} \n**Role** - {role.mention}", color=discord.Color.green())
                em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
                em.set_footer(text="USER ID: " + str(after.id))
                em.set_thumbnail(url=after.avatar_url)
                await log_chat.send(embed=em)

    if before.nick != after.nick:
        if after.nick == None:
            before.nick = before.nick
            em = discord.Embed(description=f"**Nickname removed for** - {after.mention}", color=discord.Color.blue())
            em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
            em.add_field(name="Before", value=f"{before.nick}")
            em.add_field(name="After", value=f"{after.nick}")
            em.set_thumbnail(url=after.avatar_url)
            em.set_footer(text="USER ID: " + str(after.id))
        if before.nick == None:
            before.nick = before.nick
            em = discord.Embed(description=f"**Nickname added for** - {after.mention}", color=discord.Color.blue())
            em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
            em.add_field(name="Before", value=f"{before.nick}")
            em.add_field(name="After", value=f"{after.nick}")
            em.set_thumbnail(url=after.avatar_url)
            em.set_footer(text="USER ID: " + str(after.id))
        if after.nick != None:
            if before.nick != None:
                em = discord.Embed(description=f"**Nickname changed for** - {after.mention}", color=discord.Color.blue())
                em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
                em.add_field(name="Before", value=f"{before.nick}")
                em.add_field(name="After", value=f"{after.nick}")
                em.set_thumbnail(url=after.avatar_url)
                em.set_footer(text="USER ID: " + str(after.id)) 
        await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_invite_create(invite):
    global log
    log_chat = client.get_channel(int(log))
    em = discord.Embed(title= "New invite created", color=discord.Color.green())
    em.add_field(name="Invite", value=str(invite), inline=False)
    em.add_field(name="Creater", value=str(invite.inviter.mention), inline=True)
    em.add_field(name="Channel", value=str(invite.channel.mention), inline=True)
    em.set_thumbnail(url=invite.guild.icon_url)
    em.set_footer(text="USER ID: " + str(invite.inviter.id))
    await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_invite_delete(invite):
    global log
    log_chat = client.get_channel(int(log))
    em = discord.Embed(title= "Old invite revoked", color=discord.Color.red())
    em.add_field(name="Invite", value=str(invite), inline=False)
    em.add_field(name="Channel", value=str(invite.channel), inline=True)
    em.set_thumbnail(url=invite.guild.icon_url)
    await log_chat.send(embed=em)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_guild_channel_create(channel):
    global log
    log_chat = client.get_channel(int(log))
    em = discord.Embed(title=f"Channel Created - #{channel}", color=discord.Color.green())
    em.add_field(name="Catrgory", value=f"`{channel.category}`")
    em.set_thumbnail(url=channel.guild.icon_url)
    em.set_footer(text="CHANNEL ID: " + str(channel.id))
    await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_guild_channel_delete(channel):
    global log
    log_chat = client.get_channel(int(log))
    em = discord.Embed(title=f"Channel Deleted - #{channel}", color=discord.Color.red())
    em.add_field(name="Catrgory", value=f"`{channel.category}`")
    em.set_thumbnail(url=channel.guild.icon_url)
    em.set_footer(text="CHANNEL ID: " + str(channel.id))
    await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_raw_reaction_add(payload):
    global log
    log_chat = client.get_channel(int(log))
    emoji = payload.emoji
    member = payload.member
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if member.id == 741296603733950494:
        return
    em = discord.Embed(description=f"**‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎Reaction added in {channel.mention}** - [Message]({message.jump_url})   ", color=discord.Color.green())
    em.add_field(name="Emoji", value=f"{str(emoji)}", inline=False)
    em.add_field(name="Message by", value=f"{message.author.mention}", inline=True)
    em.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
    em.set_footer(text="MESSAGE ID: " + str(message.id))
    await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_raw_reaction_remove(payload):
    global log
    log_chat = client.get_channel(int(log))
    emoji = payload.emoji
    user = payload.user_id
    member = client.get_user(user)
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    em = discord.Embed(description=f"**Reaction removed in {channel.mention}** - [Message]({message.jump_url})", color=discord.Color.red())
    em.add_field(name="Emoji", value=f"{str(emoji)}", inline=False)
    em.add_field(name="Message by", value=f"{message.author.mention}", inline=False)
    em.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
    em.set_footer(text="MESSAGE ID: " + str(message.id))
    await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_raw_reaction_clear(payload):
    global log
    log_chat = client.get_channel(int(log))
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    em = discord.Embed(title=f"Reactions Cleared", color=discord.Color.red())
    em.add_field(name="Message", value=f"[Click Here!]({message.jump_url})", inline=False)
    em.set_thumbnail(url=channel.guild.icon_url)
    await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_raw_reaction_clear_emoji(payload):
    global log
    log_chat = client.get_channel(int(log))
    emoji = payload.emoji
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    em = discord.Embed(title=f"Emoji Cleared", color=discord.Color.red())
    em.add_field(name="Emoji", value=f"{str(emoji)}", inline=False)
    em.add_field(name="Message", value=f"[Click Here!]({message.jump_url})", inline=False)
    em.set_thumbnail(url=channel.guild.icon_url)
    await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_guild_channel_update(before, after):
    global log
    log_chat = client.get_channel(int(log))
    valueb = ""
    valuea = ""
    em = discord.Embed(title=f'Channel "{before.name}" Updated', color=discord.Color.blue())
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
    await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_guild_channel_pins_update(channel, last_pin):
    global log
    log_chat = client.get_channel(int(log))
    status = "Pins Updated"
    pins = await channel.pins()
    pin = "\n".join(["[Click Here!](" + pin.jump_url + ")" for pin in pins])
    if pin == "":
        pin = None
        status = "Pins Removed"
    em = discord.Embed(title=status, color=discord.Color.blue())
    em.add_field(name="Channel", value=channel.mention)
    em.add_field(name="Pins", value=str(pin))
    em.set_thumbnail(url=channel.guild.icon_url)
    em.set_footer(text="CHANNEL ID: " + str(channel.id))
    await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_guild_update(before, after):
    global log
    log_chat = client.get_channel(int(log))
    if before.banner != after.banner:
        emold = discord.Embed(title=f"{after.name}'s' Banner Changed", description="Before", color=discord.Color.blue())
        emold.set_image(url=before.banner_url)
        emold.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emold)
        emnew = discord.Embed(title=f"{after.name}'s Banner Changed", description="After", color=discord.Color.blue())
        emnew.set_image(url=after.banner_url)
        emnew.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emnew)
    if before.name != after.name:
        em = discord.Embed(title="Server Name Changed", color=discord.Color.blue())
        em.add_field(name="Before", value=before.name, inline=False)
        em.add_field(name="After", value=after.name, inline=False)
        em.set_thumbnail(url=before.icon_url)
        em.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=em)
    if before.icon != after.icon:
        emold = discord.Embed(title=f"{after.name}'s Icon Changed", description="Before", color=discord.Color.blue())
        emold.set_image(url=before.icon_url)
        emold.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emold)
        emnew = discord.Embed(title=f"{after.name}'s Icon Changed", description="After", color=discord.Color.blue())
        emnew.set_image(url=after.icon_url)
        emnew.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emnew)
    if before.owner != after.owner:
        em = discord.Embed(title="Server Owner Changed", color=discord.Color.blue())
        em.add_field(name="Before", value=before.owner.mention, inline=False)
        em.add_field(name="After", value=after.owner.mention, inline=False)
        em.set_thumbnail(url=before.icon_url)
        em.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=em)
    if before.splash != after.splash:
        emold = discord.Embed(title=f"{after.name}'s' Splash Changed", description="Before", color=discord.Color.blue())
        emold.set_image(url=before.spash_url)
        emold.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emold)
        emnew = discord.Embed(title=f"{after.name}'s Splash Changed", description="After", color=discord.Color.blue())
        emnew.set_image(url=after.spash_url)
        emnew.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emnew)
    if before.premium_subscription_count != after.premium_subscription_count:
        if before.premium_subscription_count > after.premium_subscription_count:
            em = discord.Embed(title=f"{after.name} lost boosts", color=discord.Color.red())
            em.add_field(name="Before", value=before.premium_subscription_count, inline=False)
            em.add_field(name="After", value=after.premium_subscription_count, inline=False)
            await log_chat.send(embed=em)
        else:
            em = discord.Embed(title=f"{after.name} gained boosts", color=discord.Color.green())
            em.add_field(name="Before", value=before.premium_subscription_count, inline=False)
            em.add_field(name="After", value=after.premium_subscription_count, inline=False)
            await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_guild_role_create(role):
    global log
    log_chat = client.get_channel(int(log))
    em = discord.Embed(title=f'Role "{role.name}" Created', color=discord.Color.green())
    em.set_thumbnail(url=role.guild.icon_url)
    em.set_footer(text="ROLE ID: " + str(role.id))
    await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_guild_role_delete(role):
    global log
    log_chat = client.get_channel(int(log))
    em = discord.Embed(title=f'Role "{role.name}" Deleted', color=discord.Color.red())
    em.set_thumbnail(url=role.guild.icon_url)
    em.set_footer(text="ROLE ID: " + str(role.id))
    await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_guild_role_update(before, after):
    global log
    log_chat = client.get_channel(int(log))
    valueb = ""
    valuea = ""
    permissions = ""
    em = discord.Embed(title=f'Role "{before.name}" Updated', color=discord.Color.blue())
    if before.name != after.name:
        valueb += f"**Name** - {before.name}\n"
        valuea += f"**Name** - {after.name}\n"
    if before.color != after.color:
        valueb += f"**Color** - {str(before.color)}\n"
        valuea += f"**Color** - {str(after.color)}\n"
    if before.permissions.add_reactions != after.permissions.add_reactions:
        permissions += f"**add_reactions** `{after.permissions.add_reactions}`\n"
    if before.permissions.administrator != after.permissions.administrator:
        permissions += f"**administrator** `{after.permissions.administrator}`\n"
    if before.permissions.attach_files != after.permissions.attach_files:
        permissions += f"**attach_files** `{after.permissions.attach_files}`\n"
    if before.permissions.ban_members != after.permissions.ban_members:
        permissions += f"**ban_members** `{after.permissions.ban_members}`\n"
    if before.permissions.change_nickname != after.permissions.change_nickname:
        permissions += f"**change_nickname** `{after.permissions.change_nickname}`\n"
    if before.permissions.connect != after.permissions.connect:
        permissions += f"**connect** `{after.permissions.connect}`\n"
    if before.permissions.create_instant_invite != after.permissions.create_instant_invite:
        permissions += f"**create_instant_invite** `{after.permissions.create_instant_invite}`\n"
    if before.permissions.deafen_members != after.permissions.deafen_members:
        permissions += f"**deafen_members** `{after.permissions.deafen_members}`\n"
    if before.permissions.embed_links != after.permissions.embed_links:
        permissions += f"**embed_links** `{after.permissions.embed_links}`\n"
    if before.permissions.external_emojis != after.permissions.external_emojis:
        permissions += f"**external_emojis** `{after.permissions.external_emojis}`\n"
    if before.permissions.kick_members != after.permissions.kick_members:
        permissions += f"**kick_members** `{after.permissions.kick_members}`\n"
    if before.permissions.manage_channels != after.permissions.manage_channels:
        permissions += f"**manage_channels** `{after.permissions.manage_channels}`\n"
    if before.permissions.manage_emojis != after.permissions.manage_emojis:
        permissions += f"**manage_emojis** `{after.permissions.manage_emojis}`\n"
    if before.permissions.manage_guild != after.permissions.manage_guild:
        permissions += f"**manage_guild** `{after.permissions.manage_guild}`\n"
    if before.permissions.manage_messages != after.permissions.manage_messages:
        permissions += f"**manage_messages** `{after.permissions.manage_messages}`\n"
    if before.permissions.manage_nicknames != after.permissions.manage_nicknames:
        permissions += f"**manage_nicknames** `{after.permissions.manage_nicknames}`\n"
    if before.permissions.manage_permissions != after.permissions.manage_permissions:
        permissions += f"**manage_permissions** `{after.permissions.manage_permissions}`\n"
    if before.permissions.manage_roles != after.permissions.manage_roles:
        permissions += f"**manage_roles** `{after.permissions.manage_roles}`\n"
    if before.permissions.manage_webhooks != after.permissions.manage_webhooks:
        permissions += f"**manage_webhooks** `{after.permissions.manage_webhooks}`\n"
    if before.permissions.mention_everyone != after.permissions.mention_everyone:
        permissions += f"**mention_everyone** `{after.permissions.mention_everyone}`\n"
    if before.permissions.move_members != after.permissions.move_members:
        permissions += f"**move_members** `{after.permissions.move_members}`\n"
    if before.permissions.mute_members != after.permissions.mute_members:
        permissions += f"**mute_members** `{after.permissions.mute_members}`\n"
    if before.permissions.priority_speaker != after.permissions.priority_speaker:
        permissions += f"**priority_speaker** `{after.permissions.priority_speaker}`\n"
    if before.permissions.read_message_history != after.permissions.read_message_history:
        permissions += f"**read_message_history** `{after.permissions.read_message_history}`\n"
    if before.permissions.read_messages != after.permissions.read_messages:
        permissions += f"**read_messages** `{after.permissions.read_messages}`\n"
    if before.permissions.send_messages != after.permissions.send_messages:
        permissions += f"**send_messages** `{after.permissions.send_messages}`\n"
    if before.permissions.send_tts_messages != after.permissions.send_tts_messages:
        permissions += f"**send_tts_messages** `{after.permissions.send_tts_messages}`\n"
    if before.permissions.speak != after.permissions.speak:
        permissions += f"**speak** `{after.permissions.speak}`\n"
    if before.permissions.stream != after.permissions.stream:
        permissions += f"**stream** `{after.permissions.stream}`\n"
    if before.permissions.use_external_emojis != after.permissions.use_external_emojis:
        permissions += f"**use_external_emojis** `{after.permissions.use_external_emojis}`\n"
    if before.permissions.use_voice_activation != after.permissions.use_voice_activation:
        permissions += f"**use_voice_activation** `{after.permissions.use_voice_activation}`\n"
    if before.permissions.value != after.permissions.value:
        permissions += f"**value** `{after.permissions.value}`\n"
    if before.permissions.view_audit_log != after.permissions.view_audit_log:
        permissions += f"**view_audit_log** `{after.permissions.view_audit_log}`\n"
    if before.permissions.view_guild_insights != after.permissions.view_guild_insights:
        permissions += f"**view_guild_insights** `{after.permissions.view_guild_insights}`\n"
    if before.hoist != after.hoist:
        permissions += f"**display_seperately** `{after.hoist}`\n"
    if before.mentionable != after.mentionable:
        permissions += f"**mentionable** `{after.mentionable}`\n"
    if valuea == "":
        valuea = None
    if valueb == "":
        valueb = None
    em.add_field(name="Before", value=valueb)
    em.add_field(name="After", value=valuea)
    em.add_field(name="Permissions", value=permissions)
    em.set_thumbnail(url=before.guild.icon_url)
    em.set_footer(text="ROLE ID: " + str(before.id))
    await log_chat.send(embed=em)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_voice_state_update(member, before, after):
    global log
    log_chat = client.get_channel(int(log))
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
        em = discord.Embed(description=f"{status} - {member.mention}", color=color)
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
        em2 = discord.Embed(description=f"{status2} - {member.mention}", color=color2)
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
        em3 = discord.Embed(description=f"{status3} - {member.mention}", color=color3)
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
        em4 = discord.Embed(description=f"{status4} - {member.mention}", color=color4)
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
        em5 = discord.Embed(description=f"{status5} - {member.mention}", color=color5)
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
        em6 = discord.Embed(description=f"{status6} - {member.mention}", color=color6)
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
        em7 = discord.Embed(description=f"{status7} - {member.mention}", color=color7)
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
        em8 = discord.Embed(description=f"{status8} - {member.mention}", color=color8)
        em8.set_author(name=member, icon_url=member.avatar_url)
        em8.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em8)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_user_update(before, after):
    global log
    log_chat = client.get_channel(int(log))
    if before.avatar != after.avatar:
        emold = discord.Embed(title=f"{before.display_name}'s Avatar Updated", description="Before", color=discord.Color.blue())
        emold.set_image(url=before.avatar_url)
        emold.set_footer(text="USER ID: " + str(before.id))
        await log_chat.send(embed=emold)
        emnew = discord.Embed(title=f"{before.display_name}'s Avatar Updated", description="After", color=discord.Color.blue())
        emnew.set_image(url=after.avatar_url)
        emnew.set_footer(text="USER ID: " + str(before.id))
        await log_chat.send(embed=emnew)
    else:
        em = discord.Embed(title=f"{before.display_name}'s Name/Discriminator Updated", color=discord.Color.blue())
        em.add_field(name="Before", value=f"`{before.name}#{before.discriminator}`", inline=False)
        em.add_field(name="After", value=f"`{after.name}#{after.discriminator}`", inline=False)
        em.set_footer(text="USER ID: " + str(before.id))
        em.set_thumbnail(url=before.avatar_url)
        await log_chat.send(embed=em)











client.run('ODExMjQzMjQwODM2ODI1MDk5.YCvXJA.koWM9mPBTB5iwhKmCwPS1KHu0H0')
