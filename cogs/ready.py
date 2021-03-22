import discord
from discord.ext import commands, tasks
import re
import asyncio
import json
from datetime import datetime, timedelta
import os
import random

ban_reason = ""

class Ready(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def save(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r"C:\Users\nakul\Documents\GitHub\mybot\jsons\py.json", 'w') as f:
                json.dump(self.bot.data, f, indent=4)

            await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as")
        print(self.bot.user.name)
        print("------")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("The wait for $"))
        self.msg1.start()
        self.msg2.start()
        self.msg3.start()
        self.msg4.start()


    # Message 1
    @tasks.loop(hours=24)
    async def msg1(self):
        chn = self.bot.get_channel(821293030614368286)
        if self.bot.data['wt']['sport']['id'] != 0:
            msggggg = await chn.fetch_message(self.bot.data['wt']['sport']['id'])
            await msggggg.delete()
            self.bot.data['wt']['sport']['id'] = 0

        if self.bot.data['wt']['sport']['id2'] != 0:
            msggggggg = await chn.fetch_message(self.bot.data['wt']['sport']['id2'])
            await msggggggg.delete()
            self.bot.data['wt']['sport']['id2'] = 0


        self.bot.data['wt']['sport']["votes"]['bb'] = 0
        self.bot.data['wt']['sport']['votes']['fb'] = 0
        self.bot.data['wt']['sport']['votes']['bm'] = 0
        self.bot.data['wt']['sport']['votes']['cr'] = 0
        self.bot.data['wt']['sport']['votes']['tt'] = 0
        self.bot.data['wt']['sport']['reactants'] = {}
        chn = self.bot.get_channel(821293030614368286)
        em = discord.Embed(title="What sport would you like to play tomorrow?", description="React :basketball: for basketball, \nReact :soccer: for football, \nReact :badminton: for badminton, \nReact :cricket_game: for cricket, \nReact :ping_pong: for table tennis!")
        mes = await chn.send('@everyone', embed=em)
        await mes.add_reaction("🏀")
        await mes.add_reaction("⚽")
        await mes.add_reaction("🏸")
        await mes.add_reaction("🏏")
        await mes.add_reaction("🏓")
        await mes.add_reaction(self.bot.CROSS_MARK)
        self.bot.data['wt']['sport']['id'] = mes.id
        await self.save()

    @msg1.before_loop
    async def before_msg1(self):
        for _ in range(60*60*24):
            if datetime.now().hour == 22 and datetime.now().minute == 0:
                return
            await asyncio.sleep(1)

    # Message 2
    @tasks.loop(hours=24)
    async def msg2(self):
        chn = self.bot.get_channel(821293030614368286)
        ping = ""
        sport = ""
        for mem in self.bot.data['wt']['sport']['reactants'].keys():
            ping += mem + " "
        lst = self.bot.data['wt']['sport']['votes'].values()
        val = max(lst)
        for vote in self.bot.data['wt']['sport']['votes'].keys():
            if self.bot.data['wt']['sport']['votes'][vote] == val:
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
        mssg = await chn.send(f"{ping} - {str(len(self.bot.data['wt']['sport']['reactants'].keys()))}", embed=em)
        self.bot.data['wt']['sport']['id2'] = mssg.id
        await asyncio.sleep(5)
        if len(sport) == 78:
            s1 = sport[0:34]
            s2 = sport[34:78]
            s = [s1, s2]
            await chn.send(f"Since there was a tie of 2 sports, initiating randomizer!")
            em = discord.Embed(title="Sport for Today!", description=f"The sport picked for today is - {random.choice(s)}!")
            mssge = await chn.send(f"{ping} - {str(len(self.bot.data['wt']['sport']['reactants'].keys()))}", embed=em)
            self.bot.data['wt']['sport']['id2'] = mssge.id
            await mssg.delete()
        elif len(sport) == 112:
            s1 = sport[0:34]
            s2 = sport[34:78]
            s3 = sport[78:112]
            s = [s1, s2, s3]
            await chn.send(f"Since there was a tie of 3 sports, initiating randomizer!")
            em = discord.Embed(title="Sport for Today!", description=f"The sport picked for today is - {random.choice(s)}!")
            mssge = await chn.send(f"{ping} - {str(len(self.bot.data['wt']['sport']['reactants'].keys()))}", embed=em)
            self.bot.data['wt']['sport']['id2'] = mssge.id
            await mssg.delete()
        elif len(sport) == 156:
            s1 = sport[0:34]
            s2 = sport[34:78]
            s3 = sport[78:112]
            s4 = sport[112:156]
            s = [s1, s2, s3, s4]
            await chn.send(f"Since there was a tie of 4 sports, initiating randomizer!")
            em = discord.Embed(title="Sport for Today!", description=f"The sport picked for today is - {random.choice(s)}!")
            mssge = await chn.send(f"{ping} - {str(len(self.bot.data['wt']['sport']['reactants'].keys()))}", embed=em)
            self.bot.data['wt']['sport']['id2'] = mssge.id
            await mssg.delete()
        elif len(sport) == 190:
            s1 = sport[0:34]
            s2 = sport[34:78]
            s3 = sport[78:112]
            s4 = sport[112:156]
            s5 = sport[156:190]
            s = [s1, s2, s3, s4, s5]
            await chn.send(f"Since there was a tie of 5 sports, initiating randomizer!")
            em = discord.Embed(title="Sport for Today!", description=f"The sport picked for today is - {random.choice(s)}!")
            mssge = await chn.send(f"{ping} - {str(len(self.bot.data['wt']['sport']['reactants'].keys()))}", embed=em)
            self.bot.data['wt']['sport']['id2'] = mssge.id
            await mssg.delete()

        await self.save()

    @msg2.before_loop
    async def before_msg2(self):
        for _ in range(60*60*24):
            if datetime.now().hour == 18 and datetime.now().minute == 0:
                return
            await asyncio.sleep(1)


    # Message 3
    @tasks.loop(hours=24)
    async def msg3(self):
        chn = self.bot.get_channel(821293030614368286)
        if self.bot.data['wt']['time']['id'] != 0:
            msg = await chn.fetch_message(self.bot.data['wt']['time']['id'])
            await msg.delete()
            self.bot.data['wt']['time']['id'] = 0

        if self.bot.data['wt']['time']['id2'] != 0:
            msgg = await chn.fetch_message(self.bot.data['wt']['time']['id2'])
            await msgg.delete()
            self.bot.data['wt']['time']['id2'] = 0


        self.bot.data['wt']['time']["votes"]['65'] = 0
        self.bot.data['wt']['time']['votes']['70'] = 0
        self.bot.data['wt']['time']['votes']['75'] = 0
        self.bot.data['wt']['time']['votes']['80'] = 0
        self.bot.data['wt']['time']['votes']['85'] = 0
        self.bot.data['wt']['time']['reactants'] = {}
        chn = self.bot.get_channel(821293030614368286)
        em = discord.Embed(title="What time would you like to play tomorrow?", description="React :clock630: for 6:30, \nReact :clock7: for 7:00, \nReact :clock730: for 7:30, \nReact :clock8: for 8:00, \nReact :clock830: for 8:30!")
        mes = await chn.send('@everyone', embed=em)
        await mes.add_reaction("🕡")
        await mes.add_reaction("🕖")
        await mes.add_reaction("🕢")
        await mes.add_reaction("🕗")
        await mes.add_reaction("🕣")
        await mes.add_reaction(self.bot.CROSS_MARK)
        self.bot.data['wt']['time']['id'] = mes.id
        await self.save()

    @msg3.before_loop
    async def before_msg3(self):
        for _ in range(60*60*24):
            if datetime.now().hour == 22 and datetime.now().minute == 0:
                return
            await asyncio.sleep(1)

    # Message 4
    @tasks.loop(hours=24)
    async def msg4(self):
        chn = self.bot.get_channel(821293030614368286)
        ping = ""
        time = ""
        for mem in self.bot.data['wt']['time']['reactants'].keys():
            ping += mem
        lst = self.bot.data['wt']['time']['votes'].values()
        val = max(lst)
        for vote in self.bot.data['wt']['time']['votes'].keys():
            if self.bot.data['wt']['time']['votes'][vote] == val:
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
        mssg = await chn.send(f"{ping} - {str(len(self.bot.data['wt']['time']['reactants'].keys()))}", embed=em)
        self.bot.data['wt']['time']['id2'] = mssg.id
        await asyncio.sleep(5)
        if len(sport) == 12:
            s1 = sport[0:6]
            s2 = sport[6:12]
            s = [s1, s2]
            print(s)
            await chn.send(f"Since there was a tie of 2 timings, initiating randomizer!")
            em = discord.Embed(title="Time for Today!", description=f"The time picked for today is - {random.choice(s)}!")
            mssge = await chn.send(f"{ping} - {str(len(self.bot.data['wt']['time']['reactants'].keys()))}", embed=em)
            self.bot.data['wt']['time']['id2'] = mssge.id
            await mssg.delete()
        elif len(sport) == 18:
            s1 = sport[0:6]
            s2 = sport[6:12]
            s3 = sport[12:18]
            s = [s1, s2, s3]
            await chn.send(f"Time there was a tie of 3 timings, initiating randomizer!")
            em = discord.Embed(title="Time for Today!", description=f"The time picked for today is - {random.choice(s)}!")
            mssge = await chn.send(f"{ping} - {str(len(self.bot.data['wt']['time']['reactants'].keys()))}", embed=em)
            self.bot.data['wt']['time']['id2'] = mssge.id
            await mssg.delete()
        elif len(sport) == 24:
            s1 = sport[0:6]
            s2 = sport[6:12]
            s3 = sport[12:18]
            s4 = sport[18:24]
            s = [s1, s2, s3, s4]
            await chn.send(f"Time there was a tie of 4 timings, initiating randomizer!")
            em = discord.Embed(title="Time for Today!", description=f"The time picked for today is - {random.choice(s)}!")
            mssge = await chn.send(f"{ping} - {str(len(self.bot.data['wt']['time']['reactants'].keys()))}", embed=em)
            self.bot.data['wt']['time']['id2'] = mssge.id
            await mssg.delete()
        elif len(sport) == 30:
            s1 = sport[0:6]
            s2 = sport[6:12]
            s3 = sport[12:18]
            s4 = sport[18:24]
            s5 = sport[24:30]
            s = [s1, s2, s3, s4, s5]
            await chn.send(f"Time there was a tie of 5 timings, initiating randomizer!")
            em = discord.Embed(title="Time for Today!", description=f"The time picked for today is - {random.choice(s)}!")
            mssge = await chn.send(f"{ping} - {str(len(self.bot.data['wt']['time']['reactants'].keys()))}", embed=em)
            self.bot.data['wt']['time']['id2'] = mssge.id
            await mssg.delete()
        
        await self.save()

    @msg4.before_loop
    async def before_msg4(self):
        for _ in range(60*60*24):
            if datetime.now().hour == 18 and datetime.now().minute == 0:
                return
            await asyncio.sleep(1)

def setup(bot):
    bot.add_cog(Ready(bot))