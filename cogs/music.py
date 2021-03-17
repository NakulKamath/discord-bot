import asyncio
import datetime as dt
import random
import re
import typing as t
from enum import Enum

import discord
import wavelink
from discord.ext import commands

dj_role = 'dj'
modde = 'none'
stopped = False
ussser = None
ussser_url = None
chnn = {}
qpr = {}
qpru = {}
votes = {}
invite = {}
bcid = {}
started = False

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def remove(self, *args):
        self._queue.remove(args)

    def get_next_track(self):
        global stopped
        if not self._queue:
            stopped = True
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1" or mode == 'one':
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        global ussser
        global ussser_url
        global qpr
        global qpru
        if not tracks:
            raise NoTracksFound
        
        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Added {tracks[0].title} to the queue!")
            await ctx.send(embed=embed)
            for track in tracks:
                qpr[track.id] = ctx.message.author.name
                qpru[track.id] = f"{ctx.message.author.avatar_url}"
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)
                embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Added {track.title} to the queue!")
                await ctx.send(embed=embed)
                qpr[track.id] = ctx.message.author.name
                qpru[track.id] = f"{ctx.message.author.avatar_url}"

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                ) + "\n *Make sure to wait for all reactions"
            ),
            colour=discord.Color.blue(),
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"The wait for $"))
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"The wait for $"))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not started == True:
            return
        global chnn
        if str(before.channel) == chnn[str(member.guild.id)]:
            if not member.bot:
                if not [m for m in before.channel.members if not m.bot]:
                    await self.get_player(member.guild).teardown()
                    await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"The wait for $"))

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f" Wavelink node `{node.identifier}` ready.")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> Music commands are not available in DMs!")
            await ctx.send(embed=embed)
            return False

        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "127.0.0.1",
                "port": 2333,
                "rest_uri": "http://127.0.0.1:2333",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "india",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name="connect", aliases=["join", 'c', 'j'])
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        global invite
        global started
        started = True
        if not hasattr(ctx.message.author.voice, 'channel'):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in a voice channel!")
            await ctx.send(embed=embed)
            return
        global chnn
        chnn[str(ctx.guild.id)] = ctx.message.author.voice.channel.name
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"Playing music for {ctx.message.author}"))
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Connected to {channel.name}!")
        inv = channel.create_invite()
        invi = inv.url
        invite[str(ctx.guild.id)] = invi
        await ctx.send(embed=embed)

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        global invite
        if isinstance(exc, AlreadyConnectedToChannel):
            embed = discord.Embed(description=f"<:cross_mark:814801897138815026> Already connected to a voice channel! - [Join!]({invite[str(ctx.guild.id)]})")
            await ctx.send(embed=embed)
        elif isinstance(exc, NoVoiceChannel):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in a voice channel!")
            await ctx.send(embed=embed)

    @commands.command(name="disconnect", aliases=["leave", 'l', 'd'])
    async def disconnect_command(self, ctx):
        global chnn
        if not hasattr(ctx.message.author.voice, 'channel'):
            return
        if chnn[str(ctx.guild.id)] != ctx.message.author.voice.channel.name:
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in the player vc!")
            await ctx.send(embed=embed)
            return
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"The wait for $"))
        player = self.get_player(ctx)
        await player.teardown()
        embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Disconnected!")
        await ctx.send(embed=embed)

    @commands.command(name="play", aliases=['add', 'start', 'p'])
    async def play_command(self, ctx, *, query: t.Optional[str]):
        global votes
        global chnn
        global invite
        global started
        started = True
        player = self.get_player(ctx)
        if not hasattr(ctx.message.author.voice, 'channel'):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in a voice channel!")
            await ctx.send(embed=embed)
            return
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"Playing music for {ctx.message.author}"))
        if not player.is_connected:
            chnn[str(ctx.guild.id)] = ctx.message.author.voice.channel.name
            channel = await player.connect(ctx)
            inv = await channel.create_invite()
            invi = inv.url
            invite[str(ctx.guild.id)] = invi
        if chnn[str(ctx.guild.id)] != ctx.message.author.voice.channel.name:
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in the player vc!")
            await ctx.send(embed=embed)
            return
        
        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Resumed!")
            await ctx.send(embed=embed)

        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"

            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> The queue is empty!")
            await ctx.send(embed=embed)
        elif isinstance(exc, NoVoiceChannel):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in a voice channel!")
            await ctx.send(embed=embed)

    @commands.command(name="pause", aliases=['halt'])
    async def pause_command(self, ctx):
        global chnn
        if not hasattr(ctx.message.author.voice, 'channel'):
            return
        if chnn[str(ctx.guild.id)] != ctx.message.author.voice.channel.name:
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in the player vc!")
            await ctx.send(embed=embed)
            return
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Paused!")
        await ctx.send(embed=embed)

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> Already paused!")
            await ctx.send(embed=embed)

    @commands.command(name="stop", aliases=['clear'])
    @commands.has_role(dj_role)
    async def stop_command(self, ctx):
        global modde
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"The wait for $"))
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Stopped!")
        await ctx.send(embed=embed)
        modde = 'none'

    @commands.command(name="next", aliases=["skip"])
    async def next_command(self, ctx):
        global dj_role
        global ussser
        global chnn
        if not hasattr(ctx.message.author.voice, 'channel'):
            return
        if chnn[str(ctx.guild.id)] != ctx.message.author.voice.channel.name:
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in the player vc!")
            await ctx.send(embed=embed)
            return
        if ussser != ctx.message.author.name:
            role = discord.utils.find(lambda m: m.name == dj_role, ctx.guild.roles)
            if role in ctx.message.author.roles:
                pass
            else:
                embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be invoker to skip!")
                await ctx.send(embed=embed)
                return

        player = self.get_player(ctx)

        if not player.queue.upcoming:
            global modde
            await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"The wait for $"))
            player = self.get_player(ctx)
            player.queue.empty()
            await player.stop()
            embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Stopped!")
            await ctx.send(embed=embed)
            modde = 'none'
            return
        player.queue.set_repeat_mode('off')
        await player.stop()
        embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Playing the next track!")
        player.queue.set_repeat_mode(modde)
        await ctx.send(embed=embed)

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> The queue is empty!")
            await ctx.send(embed=embed)
        elif isinstance(exc, NoMoreTracks):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> The queue is empty!")
            await ctx.send(embed=embed)

    @commands.command(name="previous", aliases=['prev'])
    async def previous_command(self, ctx):
        global chnn
        if not hasattr(ctx.message.author.voice, 'channel'):
            return
        if chnn[str(ctx.guild.id)] != ctx.message.author.voice.channel.name:
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in the player vc!")
            await ctx.send(embed=embed)
            return
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()
        embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Playing the previous track!")
        await ctx.send(embed=embed)

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> The queue is empty!")
            await ctx.send(embed=embed)
        elif isinstance(exc, NoPreviousTracks):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> No previous tracks in queue!")
            await ctx.send(embed=embed)

    @commands.command(name="shuffle", aliases=['shu'])
    @commands.has_role(dj_role)
    async def shuffle_command(self, ctx):
        global chnn
        if not hasattr(ctx.message.author.voice, 'channel'):
            return
        if chnn[str(ctx.guild.id)] != ctx.message.author.voice.channel.name:
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in the player vc!")
            await ctx.send(embed=embed)
            return
        player = self.get_player(ctx)
        player.queue.shuffle()
        embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Queue shuffled!")
        await ctx.send(embed=embed)

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> The queue is empty!")
            await ctx.send(embed=embed)

    @commands.command(name="repeat", aliases=['loop'])
    async def repeat_command(self, ctx, mode: str=None):
        global chnn
        if not hasattr(ctx.message.author.voice, 'channel'):
            return
        if chnn[str(ctx.guild.id)] != ctx.message.author.voice.channel.name:
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in the player vc!")
            await ctx.send(embed=embed)
            return
        global modde
        if mode == None:
            if modde == 'none':
                mode = '1'
                modde = '1'
            elif modde == '1':
                mode = 'all'
                modde = 'all'
            elif modde == 'all':
                mode = 'off'
                modde = 'none'
        if mode != None:
            if mode not in ("off", "1", "all"):
                embed = discord.Embed(description="<:cross_mark:814801897138815026> Give a mode `off`, `1` or `all` and reuse the command!")
                await ctx.send(embed=embed)
                raise InvalidRepeatMode
        if mode == "off":
            mode = "none"
        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Repeat mode - `{mode}`")
        await ctx.send(embed=embed)

    @commands.command(name="queue", aliases=['q', 'que'])
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        global chnn
        if not hasattr(ctx.message.author.voice, 'channel'):
            return
        if chnn[str(ctx.guild.id)] != ctx.message.author.voice.channel.name:
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in the player vc!")
            await ctx.send(embed=embed)
            return
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title="Queue",
            description=f"Showing up to next {show} tracks",
            colour=discord.Color.blue(),
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Currently playing",
            value=getattr(player.queue.current_track, "title", "No tracks currently playing."),
            inline=False
        )
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Next up",
                value="\n".join(t.title for t in upcoming[:show]),
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name="now_playing", aliases=['np'])
    async def now_playing_command(self, ctx):
        global chnn
        global ussser
        global ussser_url
        player = self.get_player(ctx)
        if not hasattr(player.current, 'length'):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> Not playing a track at the moment!")
            await ctx.send(embed=embed)
            return

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title="Now playing",
            colour=discord.Color.blue(),
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Requested by {ussser}", icon_url=ussser_url)

        m, s = divmod(int(player.position)//1000, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            if len(str(s)) == 1:
                s = "0"+str(s)
            pos = f"0:0:{s}"
        elif int(h) == 0 and int(m) != 0:
            if len(str(s)) == 1:
                s = "0"+str(s)
            if len(str(m)) == 1:
                m = "0"+str(m)
            pos = f"0:{m}:{s}"
        else:
            if len(str(s)) == 1:
                s = "0"+str(s)
            if len(str(m)) == 1:
                m = "0"+str(m)
            pos = f"{h}:{m}:{s}"
        
        m, s = divmod(int(player.current.length)//1000, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            if len(str(s)) == 1:
                s = "0"+str(s)
            clen = f"0:0:{s}"
        elif int(h) == 0 and int(m) != 0:
            if len(str(s)) == 1:
                s = "0"+str(s)
            if len(str(m)) == 1:
                m = "0"+str(m)
            clen = f"0:{m}:{s}"
        else:
            if len(str(s)) == 1:
                s = "0"+str(s)
            if len(str(m)) == 1:
                m = "0"+str(m)
            clen = f"{h}:{m}:{s}"

        embed.add_field(
            name="Currently playing",
            value=getattr(player.queue.current_track, "title", "No tracks currently playing."),
            inline=False
        )
        val1 = int(round(player.position/player.current.length*25))
        val2 = 25-int(round(player.position/player.current.length*25))
        if val1 > 0:
            vall=f"[{'▬'*val1}](https://discord.gg/jDMYEV5)"
        else:
            vall="▬"*val1
        embed.add_field(name=f"**Time** - `{pos}/{clen}`", value=vall + ' :radio_button: ' + "▬"*val2)

        await ctx.send(embed=embed)

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        global stopped
        if isinstance(exc, QueueIsEmpty):
            if stopped == True:
                await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"The wait for $"))
                stopped = False
            embed = discord.Embed(description=f"<:tick_mark:814801884358901770> The queue is empty!")
            await ctx.send(embed=embed)

    @wavelink.WavelinkMixin.listener()
    async def on_track_start(self, node: wavelink.node.Node, payload: wavelink.events.TrackStart):
        global ussser
        global ussser_url
        global votes
        ussser = qpr[str(payload.track)]
        ussser_url = qpru[str(payload.track)]
        votes[str(payload.player.guild_id)] = 0
    
    @commands.command(name="restart", aliases=["r"])
    async def restart_command(self, ctx):
        global dj_role
        global ussser
        global chnn
        if not hasattr(ctx.message.author.voice, 'channel'):
            return
        if chnn[str(ctx.guild.id)] != ctx.message.author.voice.channel.name:
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in the player vc!")
            await ctx.send(embed=embed)
            return
        if ussser != ctx.message.author.name:
            role = discord.utils.find(lambda m: m.name == dj_role, ctx.guild.roles)
            if role in ctx.message.author.roles:
                pass
            else:
                embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be invoker to restart!")
                await ctx.send(embed=embed)
                return
        player = self.get_player(ctx) 
        await player.seek(0)
        embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Restarted the track!")
        await ctx.send(embed=embed)

    @commands.command(name="votenext", aliases=["voteskip", 'vs'])
    async def votenext_command(self, ctx):
        global dj_role
        global ussser
        global chnn
        global votes
        if str(ctx.guild.id) not in votes.keys():
            votes[str(ctx.guild.id)] = 0
        if not hasattr(ctx.message.author.voice, 'channel'):
            return
        if chnn[str(ctx.guild.id)] != ctx.message.author.voice.channel.name:
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You must be in the player vc!")
            await ctx.send(embed=embed)
            return

        player = self.get_player(ctx)
        vcn = len(ctx.message.author.voice.channel.members) - 1
        votes[str(ctx.guild.id)] = votes[str(ctx.guild.id)] + 1
        vr = round(vcn/2)
        if vr == 0:
            vr = 1
        embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Added your vote - `{votes[str(ctx.guild.id)]}/{vr}` votes!")
        await ctx.send(embed=embed)
        if votes[str(ctx.guild.id)] >= vr:
            if not player.queue.upcoming:
                global modde
                await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"The wait for $"))
                player = self.get_player(ctx)
                player.queue.empty()
                await player.stop()
                embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Stopped!")
                await ctx.send(embed=embed)
                modde = 'none'
                votes[str(ctx.guild.id)] = 0
                return
            player.queue.set_repeat_mode('off')
            await player.stop()
            embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Playing the next track!")
            await ctx.send(embed=embed)
            player.queue.set_repeat_mode(modde)
            votes[str(ctx.guild.id)] = 0

    
    @commands.command(name="seek", aliases=['s'])
    async def seek_command(self, ctx, s: str=None, m: str=None, h: str=None):
        player = self.get_player(ctx) 
        if not hasattr(player.current, 'length'):
            embed = discord.Embed(description="<:cross_mark:814801897138815026> Not playing a track at the moment!")
            await ctx.send(embed=embed)
            return
        val = 0
        t = re.compile(r"([0-9][0-9](s|m|h))|([0-9](s|m|h))")
        if s != None and m == None and h == None:
            tts = t.match(s)
            if tts == None:
                embed = discord.Embed(description="<:cross_mark:814801897138815026> Use the syntax `XXh XXm XXs`!")
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
        elif s != None and m != None and h == None:
            tts = t.match(s)
            if tts == None:
                embed = discord.Embed(description="<:cross_mark:814801897138815026> Use the syntax `XXh XXm XXs`!")
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
            ttm = t.match(m)
            if ttm == None:
                embed = discord.Embed(description="<:cross_mark:814801897138815026> Use the syntax `XXh XXm XXs`!")
                await ctx.send(embed=embed)
                return
            tm = ttm.group()
            if tm[-1] == 's':
                tm = tm[:-1]
                val = val + int(tm)*1000
            if tm[-1] == 'm':
                tm = tm[:-1]
                val = val + int(tm)*60000
            if tm[-1] == 'h':
                tm = tm[:-1]
                val = val + int(tm)*3600000
        elif s != None and m != None and h != None:
            tts = t.match(s)
            if tts == None:
                embed = discord.Embed(description="<:cross_mark:814801897138815026> Use the syntax `XXh XXm XXs`!")
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
            ttm = t.match(m)
            if ttm == None:
                embed = discord.Embed(description="<:cross_mark:814801897138815026> Use the syntax `XXh XXm XXs`!")
                await ctx.send(embed=embed)
                return
            tm = ttm.group()
            if tm[-1] == 's':
                tm = tm[:-1]
                val = val + int(tm)*1000
            if tm[-1] == 'm':
                tm = tm[:-1]
                val = val + int(tm)*60000
            if tm[-1] == 'h':
                tm = tm[:-1]
                val = val + int(tm)*3600000
            tth = t.match(h)
            if tth == None:
                embed = discord.Embed(description="<:cross_mark:814801897138815026> Use the syntax `XXh XXm XXs`!")
                await ctx.send(embed=embed)
                return
            th = tth.group()
            if th[-1] == 's':
                th = th[:-1]
                val = val + int(th)*1000
            if th[-1] == 'm':
                th = th[:-1]
                val = val + int(th)*60000
            if th[-1] == 'h':
                th = th[:-1]
                val = val + int(th)*3600000
        if val > player.current.length:
            embed = discord.Embed(description="<:cross_mark:814801897138815026> You cannot seek past the track's length!")
            await ctx.send(embed=embed)
            return
        await player.seek(val)
        m, s = divmod(val//1000, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Seeked to - {s}s!")
            await ctx.send(embed=embed)
        elif int(h) == 0 and int(m) != 0:
            embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Seeked to - {m}m {s}s!")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"<:tick_mark:814801884358901770> Seeked to - {h}h {m}m {s}s!")
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Music(bot))