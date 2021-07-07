import discord, random, time, praw, asyncio, requests, youtube_dl, pymongo
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands, tasks
from dotenv import load_dotenv
from os import getenv, listdir


#This loads in some secret variables for the connections to discord API and Firebase API
load_dotenv()
TOKEN=getenv("DISCORD_TOKEN")


#This initialises the bot with the prefix "$"
client=commands.Bot(command_prefix="$")

#This allows me to write my own help command.
client.remove_command("help")
    

#This is just a short event that runs when the bot connects. It will print out "Bot is ready", for when I'm debugging, and also set its status to "$help"
#It also loads all the functions of the bot from the other files.
@client.event
async def on_ready():
    for file in listdir("./cogs"):
        try:
            if file.endswith(".py"):
                client.unload_extension(f"cogs.{file[0:-3]}")
                client.load_extension(f"cogs.{file[0:-3]}")
        except commands.errors.ExtensionNotLoaded:
            client.load_extension(f"cogs.{file[0:-3]}")

    print("Bot is ready")
    await client.change_presence(activity = discord.Game("$help"))


#This is a simple "no u" response function because my sense of comedy as well as my sense of self is slowly deteriorating, please send help.
#I'm just kidding of course.
@client.event
async def on_message(message):

    responses=["Still you","https://www.youtube.com/watch?v=TyfNZs2dPto",
                "ur dad", "It's not me, it's youuuuu.", "no u.", "uno reverse",
                "ur face", "undoubtedly u", "ew no", "are you 5?", "stay away from me",
                "haha you're so funny /s", "i see you've run out of responses." ]
    if ("no u " in str(message.content.lower()) and not(message.author == client.user)) or (str(message.content.lower())=="no u"):
        reply=random.choice(responses1)
        await message.channel.send(reply)
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown, you can use it in {round(error.retry_after, 2)} seconds.")


#This is a very messy and unorganised implementation of the help command.
#Actually... lemme shift all of this dictionary into a separate file.
#That's better.
@client.command()
async def help(ctx, category=None):
    embed= discord.Embed( colour = discord.Colour.blue())
    author=ctx.message.author
    embed.set_author(name="Help")
    cogs = sorted(client.cogs)
    if category==None:
        for cog in cogs:
            embed.add_field(name=f"{cog}", value="Category", inline=True)
        return await ctx.send(embed=embed)
    
    requestedCog = client.get_cog(category.capitalize())
    if requestedCog==None:        
        await ctx.send("That category does not exist.")
        return await ctx.send("Run '$help' to see all the categories.")

    cogCommands = requestedCog.get_commands()
    for command in cogCommands:
        aliases = command.aliases
        if len(aliases)==0:
            aliases="No Aliases"
        embed.add_field(name=f"{command.name}", value=f"Aliases: {aliases}", inline=False)


    await ctx.send(embed=embed)

#Always be plugging.
@client.command()
async def github(ctx):
    await ctx.send("https://github.com/EDiasAlberto/proxabot")
    

client.run(TOKEN)
