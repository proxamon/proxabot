import discord, random, time, praw, os
from discord.ext import commands
from dotenv import load_dotenv

#This loads in some secret variables for the connections to discord API and reddit API
load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")

#This initialises the bot with the prefix "$"
client=commands.Bot(command_prefix="$")

#This allows me to write my own help command.
client.remove_command("help")

#This is just a short event that runs when the bot connects. It will print out "Bot is ready", for when I'm debugging, and also set its status to "$help"
@client.event
async def on_ready():
    for file in os.listdir("./cogs"):
        try:
            if file.endswith(".py"):
                client.unload_extension(f"cogs.{file[0:-3]}")
                client.load_extension(f"cogs.{file[0:-3]}")
        except commands.errors.ExtensionNotLoaded:
            client.load_extension(f"cogs.{file[0:-3]}")

    print("Bot is ready")
    await client.change_presence(activity = discord.Game("$help"))

#This command allows my bot to join voice channels.
#Initially, I was planning to develop this, but then I just decided to use it to cope with loneliness.
@client.command()
async def join(ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

#This is for trolling ProxaBot
@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

#This is a very messy and unorganised implementation of the help command.
#Actually... lemme shift all of this dictionary into a separate file.
#That's better.
@client.command()
async def help(ctx):
    author=ctx.message.author
    embed= discord.Embed( colour = discord.Colour.blue())
    embed.set_author(name="Help")

    with open("botData/commands.txt", "r") as file:
        for line in file:
            command, helpText = line.strip(",\n").replace("\"", "").split(":")
            embed.add_field(name=f"${command}", value=helpText, inline=False)
    
    await ctx.send(author, embed=embed)

#Always be plugging.
@client.command()
async def github(ctx):
    await ctx.send("https://github.com/proxamon/proxabot")
    

client.run(TOKEN)
