import asyncio
import discord
from discord.ext import commands
import datetime

"""player attributes:
    player.start()
    player.stop()
    player.is_done()
    player.is_playing()
    player.pause()
    player.resume()
    
    player.volume
    player.error
    player.yt	        The YoutubeDL <ytdl> instance.
    player.url	        The URL that is currently playing.
    player.download_url	The URL that is currently being downloaded to ffmpeg.
    player.title	The title of the audio stream.
    player.description	The description of the audio stream.
    player.uploader	The uploader of the audio stream.
    player.upload_date	A datetime.date object of when the stream was uploaded.
    player.duration	The duration of the audio in seconds.
    player.likes	How many likes the audio stream has.
    player.dislikes	How many dislikes the audio stream has.
    player.is_live	Checks if the audio stream is currently livestreaming.
    player.views	How many views the audio stream has.
"""

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

def __init__(self, bot):
        self.bot = bot

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        upload_details = ' {0.title} uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            upload_details = upload_details + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return upload_details.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Now playing audio')
            self.current.player.start()
            await self.play_next_song.wait()
            
class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    #join user's voice channel
    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx):
        """Tells bot to join voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say("Must be in a voice channel to summon bot")
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
            await self.bot.say("Joined voice channel")
        else:
            await state.voice.move_to(summoned_channel)

        return True

    #play a song from youtube using a URL or search
    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song, can play YouTube URL, or can search YouTube"""
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            self_summoned = await ctx.invoke(self.summon)
            await self.bot.say("Loading the song please be patient..")
            if not self_summoned:
                await self.bot.say("Error trying to play song")
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            error = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, error.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            skip_count = len(state.skip_votes)
            user_input = VoiceEntry(ctx.message, player)
            await self.bot.say('Added to queue: ' + player.title)
            await self.bot.say("Duration: " + str(datetime.timedelta(seconds=player.duration)))
            await self.bot.say("Views: " + str (player.views))
            await self.bot.say("Uploader: " + str(player.uploader))
            await self.bot.say("Upload Date: " + str(player.upload_date)) 
            await self.bot.say('Skips: ' + str(skip_count))
            await state.songs.put(user_input)

    #change the volume
    @commands.command(pass_context=True, no_pm=True)
    async def vol(self, ctx, value : int):
        """Sets the bot volume (1-100)"""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))

    #pause the song
    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses currently playing song"""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()
            await self.bot.say("Audio paused")

    #resume the song
    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes playing the song"""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()
            await self.bot.say("Audio resumed")

    #stops the song, clears queue
    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and clears the queue."""
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()
            await self.bot.say("Music stopped and queue cleared")

    #skips song, needs 3 votes
    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('No audio playing')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Requester requested skipping song')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Skip vote passed, skipping song')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await self.bot.say('You have already voted to skip this song.')

    #information about the video
    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows information about audio"""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('No audio playing')
        else:
            skip_count = len(state.skip_votes)
            player = state.player
            await self.bot.say("Now playing: " + player.title)
            await self.bot.say("Duration: " + str(datetime.timedelta(seconds=player.duration)))
            await self.bot.say("Views: " + str(player.views))         
            await self.bot.say("Uploader: " + str(player.uploader))
            await self.bot.say("Upload Date: " + str(player.upload_date))  
            await self.bot.say('Skips: ' + str(skip_count))

    #disconnects from the voice channel, automatically removes songs from queue
    #use this function if queue freezes
    @commands.command(pass_context=True, no_pm=True)
    async def dc(self, ctx):
        """Disconnects from the voice channel; use this and rejoin server if audio stops playing"""
        server = ctx.message.server
        state = self.get_voice_state(server)
        
        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
            await self.bot.say("Disconnected from voice channel")
        except:
            pass
            
def setup(bot):
    bot.add_cog(Music(bot))
    print('Music is loaded')
