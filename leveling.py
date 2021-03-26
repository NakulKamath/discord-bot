import discord
from discord.ext import commands, tasks
import re
import asyncio
import json
from datetime import datetime, timedelta
import os
import random
from pymongo import MongoClient

db = "mongodb+srv://me:<password>@botdb.vfqxg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
l = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

class leveling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def save(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r"C:\Users\nakul\Documents\GitHub\mybot\jsons\py.json", 'w') as f:
                json.dump(self.bot.data, f, indent=4)

            await asyncio.sleep(1)
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel not in 
