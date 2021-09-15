import discord, random, time, praw, os, youtube_dl, nacl
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands
from dotenv import load_dotenv

serverQueues = {}

class Voice(commands.Cog):

    def __init__(self, client):
        self.client = client

    #This command allows my bot to join voice channels.
    #Initially, I was planning to develop this, but then I just decided to use it to cope with loneliness.
    #Changed my mind and now it plays a random song from the folder audioFiles
    #Changed my mind again and just removed that function because it takes up a lot of space on
    @commands.command()
    async def join(self, ctx):
        global voice 
        try:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            await ctx.send("I have joined the voice chat.")
        except AttributeError:
            await ctx.send("You must be connected to a voice channel to use this command.")

    #This uses the youtube_dl library to download a video from youtube and play the 
    @commands.command()
    async def play(self, ctx, url=None, volume=0.5):
        global voice, serverQueues
        
        print(ctx.guild.id)

        try:
            os.remove("song.wav")
            serverQueues[ctx.guild.id] = [url]
        except PermissionError:
            if url==None:
                await ctx.send("Resuming playing...")
                voice.resume()
            else:
                await ctx.send("There is currently a song playing, please wait.")
                try:
                    serverQueues[ctx.guild.id].append(url)
                except KeyError:
                    serverQueues[ctx.guild.id] = [url]
        except FileNotFoundError:
            serverQueues[ctx.guild.id] = [url]
        except Exception as e:
            print(e)

        print(serverQueues[ctx.guild.id])


        ydlOpts  = {'format': 'bestaudio/best',
                     'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                     'restrictfilenames': True,
                     'noplaylist': True,
                     'nocheckcertificate': True,
                     'ignoreerrors': False,
                     'logtostderr': False,
                     'quiet': True,
                     'no_warnings': True,
                     'default_search': 'auto',
                     'source_address': '0.0.0.0',
                     'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'wav',
                        'preferredquality': '192', }]
                    }

        channel = ctx.author.voice.channel
        if ctx.voice_client is None:    
            voice = await channel.connect()
        with youtube_dl.YoutubeDL(ydlOpts) as ydl:
            try:
                ydl.download([serverQueues[ctx.guild.id][0]])
                serverQueues[ctx.guild.id].remove(url)
            except TypeError:
                await ctx.send("Error: Nothing to play")
                return

        for file in os.listdir("./"):
            if file.endswith(".wav"):
                os.rename(file, "song.wav")
        
        chosenSong = FFmpegPCMAudio("song.wav")
        voice.play(chosenSong)
        voice.source = PCMVolumeTransformer(voice.source)
        voice.source.volume= volume

    @commands.command()
    async def pause(self, ctx):
        global voice
        try:
            voice.pause()
        except Exception as e:
            print(e)
            
    @commands.command()
    async def resume(self, ctx):
        global voice
        try:
            voice.resume()
            await ctx.send("Resuming playing...")
        except Exception as e:
            print(e)

    @commands.command()
    async def stop(self, ctx):
        global voice 
        try:
            voice.stop()
            serverQueues[ctx.guild.id] = []
        except Exception as e:
            print(e)






    #This is for trolling ProxaBot
    @commands.command()
    async def leave(self, ctx):
        global voice
        await ctx.voice_client.disconnect()
        voice = None




def setup(client):
    for command in commands.Cog.get_commands(Voice):
        client.remove_command(command.name)
    client.add_cog(Voice(client))
