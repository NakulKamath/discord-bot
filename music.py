import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import shutil
import asyncio

queues = {}

class Music(commands.Cog):
    def __init__(self, bot):        
        self.bot = bot


    @commands.command(pass_context=True)
    async def join(self, context):
        global voice
        if hasattr(context.message.author.voice, 'channel'):
            channel = context.message.author.voice.channel
        else:
            em = discord.Embed(description=f"{self.bot.CROSS_MARK} You are not in any voice channell!")
            await context.send(embed=em)
            return
        voice = get(self.bot.voice_clients, guild=context.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        
        em = discord.Embed(description=f"{self.bot.TICK_MARK} Connected to {channel}!")
        await context.send(embed=em)

    @commands.command(pass_context=True)
    async def leave(self, context):
        global voice
        if hasattr(context.message.author.voice, 'channel'):
            channel = context.message.author.voice.channel
        else:
            em = discord.Embed(description=f"{self.bot.CROSS_MARK} You are not in any voice channell!")
            await context.send(embed=em)
            return
        voice = get(self.bot.voice_clients, guild=context.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            em = discord.Embed(description=f"{self.bot.TICK_MARK} Disconnected from {channel}!")
            await context.send(embed=em)
        
    @commands.command(pass_context=True)
    async def play(self, context, url: str):
        global voice
        global queues
        voice = get(self.bot.voice_clients, guild=context.guild)
        if not hasattr(voice, 'is_connected'):
            if hasattr(context.message.author.voice, 'channel'):
                channel = context.message.author.voice.channel
            else:
                em = discord.Embed(description=f"{self.bot.CROSS_MARK} You are not in any voice channell!")
                await context.send(embed=em)
                return
            voice = get(self.bot.voice_clients, guild=context.guild)

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
            
            em = discord.Embed(description=f"{self.bot.TICK_MARK} Connected to {channel}!")
            await context.send(embed=em)
        def check_queue():
            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    print(still_q)
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'song.mp3')

                    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.7

                else:
                    queues.clear()
                    return
            else:
                queues.clear()
                print("No queued songs")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there == True:
                os.remove("song.mp3")
                queues.clear()
                print("Removed old song")
        except PermissionError:
            em = discord.Embed(description=f"{self.bot.CROSS_MARK} Use `$add` instead to add a song!")
            await context.send(embed=em)
            return

        Queue_infile = os.path.isdir('Queue')

        try:
            Queue_folder = "./Queue"
            if Queue_folder is True:
                shutil.rmtree(Queue_folder)
        except:
            print("No queue folder!")
        
        em = discord.Embed(description=f"{self.bot.TICK_MARK} Starting the track!")
        await context.send(embed=em)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': "384",
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("downloading track")
            ydl.download([url])

        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file
                print(f"Renamed file: {file}")
                asyncio.sleep(5)
                os.rename(file, "song.mp3")

        voice = get(self.bot.voice_clients, guild=context.guild)
        
        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.7

        name = name.rsplit("-", 2)
        print("playing")
        
    @commands.command(pass_context=True)
    async def pause(self, context):
        voice = get(self.bot.voice_clients, guild=context.guild)

        if voice and voice.is_playing():
            voice.pause()
            em = discord.Embed(description=f"{self.bot.TICK_MARK} Paused the track!")
            await context.send(embed=em)
        elif voice and voice.is_paused():
            em = discord.Embed(description=f"{self.bot.CROSS_MARK} Track already paused!")
            await context.send(embed=em)
        else:
            em = discord.Embed(description=f"{self.bot.CROSS_MARK} There isn't anything playing!")
            await context.send(embed=em)

    @commands.command(pass_context=True)
    async def resume(self, context):
        voice = get(self.bot.voice_clients, guild=context.guild)

        if voice and voice.is_paused():
            voice.resume()
            em = discord.Embed(description=f"{self.bot.TICK_MARK} Resumed the track!")
            await context.send(embed=em)
        elif voice and voice.is_playing():
            em = discord.Embed(description=f"{self.bot.TICK_MARK} Track is already playing!")
            await context.send(embed=em)
        else:
            em = discord.Embed(description=f"{self.bot.CROSS_MARK} There isn't anything playing!")
            await context.send(embed=em)

    @commands.command(pass_context=True)
    async def skip(self, context):
        voice = get(self.bot.voice_clients, guild=context.guild)

        if voice and voice.is_playing():
            voice.stop()
            em = discord.Embed(description=f"{self.bot.TICK_MARK} Skipped the track!")
            await context.send(embed=em)
        elif voice and voice.is_paused():
            voice.stop()
            em = discord.Embed(description=f"{self.bot.TICK_MARK} Skipped the paused track!")
            await context.send(embed=em)
        else:
            em = discord.Embed(description=f"{self.bot.CROSS_MARK} There isn't anything playing!")
            await context.send(embed=em)

    @commands.command(pass_context=True)
    async def stop(self, context):
        global queues
        if voice and voice.is_playing():
            voice.stop()
            queues.clear()
            em = discord.Embed(description=f"{self.bot.TICK_MARK} Stopped the track and cleared the queue!")
            await context.send(embed=em)
        elif voice and voice.is_paused():
            voice.stop()
            queues.clear()
            em = discord.Embed(description=f"{self.bot.TICK_MARK} Stopped the paused track and cleared the queue!")
            await context.send(embed=em)
        else:
            em = discord.Embed(description=f"{self.bot.CROSS_MARK} There isn't anything playing!")
            await context.send(embed=em)



    @commands.command(pass_context=True)
    async def add(self, context, url: str):
        global queues
        Queue_infile = os.path.isdir('./Queue')
        if Queue_infile is False:
            os.mkdir("Queue")
        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in  queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num

        queue_path = os.path.abspath(os.path.realpath("Queue")) + f"\song{q_num}.%(ext)s"

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': "384",
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("downloading track")
            ydl.download([url])
        em = discord.Embed(description=f"{self.bot.TICK_MARK} Added track to queue!")
        await context.send(embed=em)

def setup(bot):
    bot.add_cog(Music(bot))