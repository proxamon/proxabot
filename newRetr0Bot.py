import discord
import random
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")


client=commands.Bot(command_prefix="$")

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_message(message):
    responses=["Still you","https://www.youtube.com/watch?v=TyfNZs2dPto", "ur dad", "It's not me, it's youuuuu.", "no u.", "uno reverse", "ur face", "don't be a cuck", "undoubtedly u" ]
    if "no u" in str(message.content.lower()) and not(message.author == client.user):
        reply=random.choice(responses)
        await message.channel.send(reply)
    await client.process_commands(message)



client.remove_command("help")


@client.command()
async def help(ctx):
    author=ctx.message.author
    commands={"ping":" Returns the latency",
              "8ball":"Returns advice for the question supplied.",
              "spam":"Types an inputted string of text an inputted number of times.",
              "clear":"Deletes a specified number of messages",
              "hi":"Sends a friendly greeting",
              "kick":"Kicks a member",
              "ban":"Bans a member"}
    embed= discord.Embed( colour = discord.Colour.blue())
    embed.set_author(name="Help")
    for x in commands:
        embed.add_field(name=f"${x}", value=commands[x], inline=False)
    await ctx.send(author, embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command(aliases=["8ball", "advice", "chance"])
async def _8ball(ctx, *, question):
    responses=["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful.",
                 "Absolutely",
                 "I believe so",
                 "My response is undecided.",
                 "I can't say.",
                 "Do what you feel is best.",
                 "You need Jesus for that."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command(aliases = ["hello", "Hi", "Hey", "Hello", "hey"])
async def hi(ctx):
    await ctx.send(f'Hello there, {ctx.message.author}')


@client.command()
@commands.has_permissions(manage_messages=True)
async def spam(ctx,*,string):
    number=string.split(" ",1)
    try:
        if int(number[0])<=20:
            for num in range(int(number[0])):
                await ctx.send(number[1])
        else:
            await ctx.send("That is too much.")
    except ValueError:
        await ctx.send("Format for spam: Command, number of times to spam, string to spam.")
        await ctx.send("For example, '$spam 10 I am a bot.'")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number=5):
    if number<=20:
        await ctx.channel.purge(limit=number+1)
    elif number>20:
        await ctx.send("Maximum 20 messages can be deleted.")
    else:
        await ctx.send("Invalid number of messages.")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, * , reason = None):
    await member.kick(reason=reason)



@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, * , reason = None):
    await member.ban(reason=reason)


client.run(TOKEN)
