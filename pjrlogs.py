import discord
from discord.ext import commands, tasks
import re
import asyncio
import json
from datetime import datetime, timedelta
import os
import random

ban_reason = ""
logs = 780319350041083904

class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_connect(self):
        print('Connected to discord!')
    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id):
        print('Connect on shard ID - ' + shard_id)
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):  
        before = payload.cached_message
        channel = self.bot.get_channel(payload.channel_id)
        after = await channel.fetch_message(payload.message_id)
        global logs
        log_chat = self.bot.get_channel(logs)
        bc = f'{self.bot.CROSS_MARK} Not in Memory!'
        if hasattr(before, 'content'):
            if len(before.content) > 1024:
                before.content = before.content[0:1020] + "\n..."
            if len(after.content) > 1024:
                after.content = before.content[0:1020] + "\n..."
            bc = before.content
        if str(after.content) == "":
            return
        if after.author == self.bot.user:
            return
        em = discord.Embed(description=f"**Message edited in {str(channel.mention)}** - [Message]({after.jump_url})", color=discord.Color.purple(), timestamp=datetime.utcnow())
        em.add_field(name=f"**Before**", value=str(bc), inline=False)
        em.add_field(name=f"**After**", value=str(after.content), inline=False)
        em.set_author(name=str(after.author), icon_url=after.author.avatar_url)
        em.set_footer(text="MESSAGE ID: " + str(after.id))
        await log_chat.send(embed=em)
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        message = payload.cached_message
        global logs
        log_chat = self.bot.get_channel(logs)
        bc = f'{self.bot.CROSS_MARK} Not in Memory!'
        auth = ""
        if hasattr(message, 'content'):
            if len(message.content) > 1024:
                message.content = message.content[0:1020] + "\n..."
            if str(message.content) == "":
                return
            bc = message.content
        if hasattr(message, 'author'):
            auth =  f" - {message.author.mention}"
        channel = self.bot.get_channel(payload.channel_id)
        em = discord.Embed(description=f"**Message deleted in {str(channel.mention)}**\n{bc}{auth}", color=discord.Color.red(), timestamp=datetime.utcnow())
        if hasattr(message, 'author'):
            em.set_author(name=str(message.author), icon_url=message.author.avatar_url)
        if hasattr(message, 'id'):
            em.set_footer(text="MESSAGE ID: " + str(message.id))
        await log_chat.send(embed=em)
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        global logs
        log_chat = self.bot.get_channel(logs)
        messages = payload.cached_messages
        message_contents = "\n".join([str(message.author.mention)+" : "+message.content for message in messages])
        channel = self.bot.get_channel(int(payload.channel_id))
        em = discord.Embed(description=f"**Bulk message delete in {str(channel.mention)}** \n {str(message_contents)}", color=discord.Color.red(), timestamp=datetime.utcnow())
        em.set_footer(text="CHANNEL ID: " + str(channel.id))
        await log_chat.send(embed=em)

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global logs
        log_chat = self.bot.get_channel(logs)
        emoji = payload.emoji
        member = payload.member
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if member.id == self.bot.user.id:
            return
        em = discord.Embed(description=f"**‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎Reaction added in {channel.mention}** - [Message]({message.jump_url})   ", color=discord.Color.green(), timestamp=datetime.utcnow())
        em.add_field(name="Emoji", value=f"{str(emoji)}", inline=False)
        em.add_field(name="Message by", value=f"{message.author.mention}", inline=True)
        em.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
        em.set_footer(text="MESSAGE ID: " + str(message.id))
        await log_chat.send(embed=em)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        global logs
        log_chat = self.bot.get_channel(logs)
        emoji = payload.emoji
        user = payload.user_id
        member = self.bot.get_user(user)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        em = discord.Embed(description=f"**Reaction removed in {channel.mention}** - [Message]({message.jump_url})", color=discord.Color.red(), timestamp=datetime.utcnow())
        em.add_field(name="Emoji", value=f"{str(emoji)}", inline=False)
        em.add_field(name="Message by", value=f"{message.author.mention}", inline=False)
        em.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
        em.set_footer(text="MESSAGE ID: " + str(message.id))
        await log_chat.send(embed=em)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_raw_reaction_clear(self, payload):
        global logs
        log_chat = self.bot.get_channel(logs)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        em = discord.Embed(title=f"Reactions Cleared", color=discord.Color.red(), timestamp=datetime.utcnow())
        em.add_field(name="Message", value=f"[Click Here!]({message.jump_url})", inline=False)
        em.set_thumbnail(url=channel.guild.icon_url)
        await log_chat.send(embed=em)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_raw_reaction_clear_emoji(self, payload):
        global logs
        log_chat = self.bot.get_channel(logs)
        emoji = payload.emoji
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        em = discord.Embed(title=f"Emoji Cleared", color=discord.Color.red(), timestamp=datetime.utcnow())
        em.add_field(name="Emoji", value=f"{str(emoji)}", inline=False)
        em.add_field(name="Message", value=f"[Click Here!]({message.jump_url})", inline=False)
        em.set_thumbnail(url=channel.guild.icon_url)
        await log_chat.send(embed=em)
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        global logs
        log_chat = self.bot.get_channel(logs)
        em = discord.Embed(title=f"Channel Created - #{channel}", color=discord.Color.green(), timestamp=datetime.utcnow())
        em.add_field(name="Category", value=f"`{channel.category}`")
        em.set_thumbnail(url=channel.guild.icon_url)
        em.set_footer(text="CHANNEL ID: " + str(channel.id))
        await log_chat.send(embed=em)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        global logs
        log_chat = self.bot.get_channel(logs)
        em = discord.Embed(title=f"Channel Deleted - #{channel}", color=discord.Color.red(), timestamp=datetime.utcnow())
        em.add_field(name="Category", value=f"`{channel.category}`")
        em.set_thumbnail(url=channel.guild.icon_url)
        em.set_footer(text="CHANNEL ID: " + str(channel.id))
        await log_chat.send(embed=em)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        global logs
        log_chat = self.bot.get_channel(logs)
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
        if hasattr(before, 'topic') or hasattr(after, 'topic'):
            if before.topic != after.topic:
                if before.topic == "":
                    valueb += "None\n"
                    valuea += f"**Topic added - ** {after.topic}\n"
                elif after.topic == "":
                    valueb += "None\n"
                    valuea += f"**Topic removed - ** {before.topic}\n"
                else:
                    valueb += f"**Topic - ** {before.topic}\n"
                    valuea += f"**Topic - ** {after.topic}\n"
        em.add_field(name="Before", value=valueb)
        em.add_field(name="After", value=valuea)
        em.set_thumbnail(url=before.guild.icon_url)
        em.set_footer(text="ROLE ID: " + str(before.id))
        if valuea != "" and valueb != "":
            await log_chat.send(embed=em)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        global logs
        log_chat = self.bot.get_channel(logs)
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
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_integrations_update(self, guild):
        global logs
        log_chat = self.bot.get_channel(logs)
        inte = await guild.integrations
        em = discord.Embed(title='Integrations', description=inte, color=discord.Color.blue(), timestamp=datetime.utcnow())
        await log_chat.send(embed=em)
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
        global logs
        log_chat = self.bot.get_channel(logs)
        inte = await channel.webhooks
        em = discord.Embed(title='Integrations', description=inte, color=discord.Color.blue(), timestamp=datetime.utcnow())
        await log_chat.send(embed=em)
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_member_join(self, member):
        global logs
        log_chat = self.bot.get_channel(logs)
        date_format = "%a, %d %b %Y %I:%M %p"
        em = discord.Embed(description= f"**Member Joined** - {member.mention}", color=discord.Color.green(), timestamp=datetime.utcnow())
        em.set_author(name=str(member), icon_url=member.avatar_url)
        em.add_field(name="Joined", value=member.joined_at.strftime(date_format))  
        members = sorted(member.guild.members, key=lambda m: m.joined_at)
        em.add_field(name="Join position", value=str(members.index(member)+1))
        em.add_field(name="Registered", value=member.created_at.strftime(date_format), inline=False)
        em.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em)
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        global logs
        log_chat = self.bot.get_channel(logs)
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
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        global logs
        log_chat = self.bot.get_channel(logs)
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
            return
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        global logs
        log_chat = self.bot.get_channel(logs)
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
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        global logs
        log_chat = self.bot.get_channel(logs)
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
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        global logs
        log_chat = self.bot.get_channel(logs)
        em = discord.Embed(title=f'Role "{role.name}" Created', color=discord.Color.green(), timestamp=datetime.utcnow())
        em.set_thumbnail(url=role.guild.icon_url)
        em.set_footer(text="ROLE ID: " + str(role.id))
        await log_chat.send(embed=em)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        global logs
        log_chat = self.bot.get_channel(logs)
        em = discord.Embed(title=f'Role "{role.name}" Deleted', color=discord.Color.red(), timestamp=datetime.utcnow())
        em.set_thumbnail(url=role.guild.icon_url)
        em.set_footer(text="ROLE ID: " + str(role.id))
        await log_chat.send(embed=em)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        global logs
        log_chat = self.bot.get_channel(logs)
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
                emoji = self.bot.TICK_MARK
            if after.permissions.add_reactions == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**add_reactions** `{after.permissions.add_reactions}`\n"
        if before.permissions.administrator != after.permissions.administrator:
            if after.permissions.administrator == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.administrator == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**administrator** `{after.permissions.administrator}`\n"
        if before.permissions.attach_files != after.permissions.attach_files:
            if after.permissions.attach_files == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.attach_files == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**attach_files** `{after.permissions.attach_files}`\n"
        if before.permissions.ban_members != after.permissions.ban_members:
            if after.permissions.ban_members == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.ban_members == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**ban_members** `{after.permissions.ban_members}`\n"
        if before.permissions.change_nickname != after.permissions.change_nickname:
            if after.permissions.change_nickname == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.change_nickname == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**change_nickname** `{after.permissions.change_nickname}`\n"
        if before.permissions.connect != after.permissions.connect:
            if after.permissions.connect == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.connect == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**connect** `{after.permissions.connect}`\n"
        if before.permissions.create_instant_invite != after.permissions.create_instant_invite:
            if after.permissions.create_instant_invite == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.create_instant_invite == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**create_instant_invite** `{after.permissions.create_instant_invite}`\n"
        if before.permissions.deafen_members != after.permissions.deafen_members:
            if after.permissions.deafen_members == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.deafen_members == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**deafen_members** `{after.permissions.deafen_members}`\n"
        if before.permissions.embed_links != after.permissions.embed_links:
            if after.permissions.embed_links == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.embed_links == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**embed_links** `{after.permissions.embed_links}`\n"
        if before.permissions.external_emojis != after.permissions.external_emojis:
            if after.permissions.external_emojis == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.external_emojis == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**external_emojis** `{after.permissions.external_emojis}`\n"
        if before.permissions.kick_members != after.permissions.kick_members:
            if after.permissions.kick_members == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.kick_members == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**kick_members** `{after.permissions.kick_members}`\n"
        if before.permissions.manage_channels != after.permissions.manage_channels:
            if after.permissions.manage_channels == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.manage_channels == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**manage_channels** `{after.permissions.manage_channels}`\n"
        if before.permissions.manage_emojis != after.permissions.manage_emojis:
            if after.permissions.manage_emojis == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.manage_emojis == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**manage_emojis** `{after.permissions.manage_emojis}`\n"
        if before.permissions.manage_guild != after.permissions.manage_guild:
            if after.permissions.manage_guild == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.manage_guild == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**manage_guild** `{after.permissions.manage_guild}`\n"
        if before.permissions.manage_messages != after.permissions.manage_messages:
            if after.permissions.manage_messages == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.manage_messages == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**manage_messages** `{after.permissions.manage_messages}`\n"
        if before.permissions.manage_nicknames != after.permissions.manage_nicknames:
            if after.permissions.manage_nicknames == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.manage_nicknames == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**manage_nicknames** `{after.permissions.manage_nicknames}`\n"
        if before.permissions.manage_permissions != after.permissions.manage_permissions:
            if after.permissions.manage_permissions == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.manage_permissions == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**manage_permissions** `{after.permissions.manage_permissions}`\n"
        if before.permissions.manage_roles != after.permissions.manage_roles:
            if after.permissions.manage_roles == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.manage_roles == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**manage_roles** `{after.permissions.manage_roles}`\n"
        if before.permissions.manage_webhooks != after.permissions.manage_webhooks:
            if after.permissions.manage_webhooks == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.manage_webhooks == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**manage_webhooks** `{after.permissions.manage_webhooks}`\n"
        if before.permissions.mention_everyone != after.permissions.mention_everyone:
            if after.permissions.mention_everyone == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.mention_everyone == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**mention_everyone** `{after.permissions.mention_everyone}`\n"
        if before.permissions.move_members != after.permissions.move_members:
            if after.permissions.move_members == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.move_members == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**move_members** `{after.permissions.move_members}`\n"
        if before.permissions.mute_members != after.permissions.mute_members:
            if after.permissions.mute_members == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.mute_members == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**mute_members** `{after.permissions.mute_members}`\n"
        if before.permissions.priority_speaker != after.permissions.priority_speaker:
            if after.permissions.priority_speaker == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.priority_speaker == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**priority_speaker** `{after.permissions.priority_speaker}`\n"
        if before.permissions.read_message_history != after.permissions.read_message_history:
            if after.permissions.read_message_history == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.read_message_history == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**read_message_history** `{after.permissions.read_message_history}`\n"
        if before.permissions.read_messages != after.permissions.read_messages:
            if after.permissions.read_messages == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.read_messages == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**read_messages** `{after.permissions.read_messages}`\n"
        if before.permissions.send_messages != after.permissions.send_messages:
            if after.permissions.send_messages == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.send_messages == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**send_messages** `{after.permissions.send_messages}`\n"
        if before.permissions.send_tts_messages != after.permissions.send_tts_messages:
            if after.permissions.send_tts_messages == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.send_tts_messages == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**send_tts_messages** `{after.permissions.send_tts_messages}`\n"
        if before.permissions.speak != after.permissions.speak:
            if after.permissions.speak == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.speak == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**speak** `{after.permissions.speak}`\n"
        if before.permissions.stream != after.permissions.stream:
            if after.permissions.stream == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.stream == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**stream** `{after.permissions.stream}`\n"
        if before.permissions.use_external_emojis != after.permissions.use_external_emojis:
            if after.permissions.use_external_emojis == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.use_external_emojis == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**use_external_emojis** `{after.permissions.use_external_emojis}`\n"
        if before.permissions.use_voice_activation != after.permissions.use_voice_activation:
            if after.permissions.use_voice_activation == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.use_voice_activation == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**use_voice_activation** `{after.permissions.use_voice_activation}`\n"
        if before.permissions.view_audit_log != after.permissions.view_audit_log:
            if after.permissions.view_audit_log == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.view_audit_log == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**view_audit_log** `{after.permissions.view_audit_log}`\n"
        if before.permissions.view_guild_insights != after.permissions.view_guild_insights:
            if after.permissions.view_guild_insights == True:
                emoji = self.bot.TICK_MARK
            if after.permissions.view_guild_insights == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**view_guild_insights** `{after.permissions.view_guild_insights}`\n"
        if before.hoist != after.hoist:
            if after.hoist == True:
                emoji = self.bot.TICK_MARK
            if after.hoist == False:
                emoji = self.bot.CROSS_MARK 
            permissions += f"{emoji}**display_seperately** `{after.hoist}`\n"
        if before.mentionable != after.mentionable:
            if after.mentionable == True:
                emoji = self.bot.TICK_MARK
            if after.mentionable == False:
                emoji = self.bot.CROSS_MARK 
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
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        global logs
        log_chat = self.bot.get_channel(logs)
        if len(before) > len(after):
            em = discord.Embed(title= "Emoji removed", color=discord.Color.red(), timestamp=datetime.utcnow())
            for x in before and not after:
                em.add_field(name='Emoji', value=str(x))
        if len(after) > len(before):
            em = discord.Embed(title= "Emoji added", color=discord.Color.red(), timestamp=datetime.utcnow())
            for x in after and not before:
                em.add_field(name='Emoji', value=str(x))
        await log_chat.send(emoji=em)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        global logs
        log_chat = self.bot.get_channel(logs)
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
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        global logs
        log_chat = self.bot.get_channel(logs)
        em = discord.Embed(description=f"**Member banned**\n {user.mention}", color=discord.Color.red(), timestamp=datetime.utcnow())
        if ban_reason != "":
            em.add_field(name="Reason", value=str(ban_reason))
        em.set_author(name=user.name + "#" + user.discriminator, icon_url=user.avatar_url)
        em.set_thumbnail(url=user.avatar_url)
        await log_chat.send(embed=em)
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        global logs
        log_chat = self.bot.get_channel(logs)
        em = discord.Embed(description=f"**Member unbanned**\n {user.mention}", color=discord.Color.green(), timestamp=datetime.utcnow())
        em.set_author(name=user.name + "#" + user.discriminator, icon_url=user.avatar_url)
        em.set_thumbnail(url=user.avatar_url)
        await log_chat.send(embed=em)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        global logs
        log_chat = self.bot.get_channel(logs)
        em = discord.Embed(title= "New invite created", color=discord.Color.green(), timestamp=datetime.utcnow())
        em.add_field(name="Invite", value=str(invite), inline=False)
        em.add_field(name="Creater", value=str(invite.inviter.mention), inline=True)
        em.add_field(name="Channel", value=str(invite.channel.mention), inline=True)
        em.set_thumbnail(url=invite.guild.icon_url)
        em.set_footer(text="USER ID: " + str(invite.inviter.id))
        await log_chat.send(embed=em)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        global logs
        log_chat = self.bot.get_channel(logs)
        em = discord.Embed(title= "Old invite revoked", color=discord.Color.red(), timestamp=datetime.utcnow())
        em.add_field(name="Invite", value=str(invite), inline=False)
        em.add_field(name="Channel", value=str(invite.channel), inline=True)
        em.set_thumbnail(url=invite.guild.icon_url)
        await log_chat.send(embed=em)

def setup(bot):
    bot.add_cog(Logging(bot))