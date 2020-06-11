import discord
import random
from discord.ext import commands
import os
from dotenv import load_dotenv
import time

load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")


client=commands.Bot(command_prefix="$")

@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(activity = discord.Game("$help"))

@client.event
async def on_message(message):
    responses1=["Still you","https://www.youtube.com/watch?v=TyfNZs2dPto", "ur dad", "It's not me, it's youuuuu.", "no u.", "uno reverse", "ur face", "don't be a cuck", "undoubtedly u" ]
    responses2=["The pleasure's all mine.", "No problem!", "You are very welcome.", "At least someone says thank you.", "Your gratitude is much appreciated.", "There's no need to thank me."]
    if "no u" in str(message.content.lower()) and not(message.author == client.user):
        reply=random.choice(responses1)
        await message.channel.send(reply)
    #elif "thank" in str(message.content.lower()) and not(message.author == client.user):
        #reply=random.choice(responses2)
        #await message.channel.send(reply)
    #if random.randint(0, 10)==7:
    #    await message.channel.send("Pokemon Spawned")
    await client.process_commands(message)


@client.command()
async def test(ctx):
    await ctx.send("Test successfull.")

@client.command(aliases = ["reeee", "ree", "reeeee"])
async def reee(ctx):
    await ctx.send("REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

@client.command()
async def save(ctx):
    number = random.randint(0,10)
    if number>8:
        await ctx.send("You have been saved.")
    else:
        await ctx.send("Leave me alone, I have better things to do.")

@client.command()
async def topic(ctx):
    starters=["What are the top three things on your bucket list?",
              "How do you think you will die?",
              "What has been the lowest point of your life?",
              "If you could ask for a miracle, what would it be?",
              "Where do you see yourself in five years?",
              "What is the biggest risk you’ve ever taken?",
              "What would your ideal life look like?",
              "If someone gave you an envelope with your death date inside of it, would you open it?",
              "When have you been the most happy?",
              "Do you know anyone who is living their life to the fullest?",
              "What is your idea of the perfect day?",
              "Who has been the most influential person in your life and why?",
              "What book had a big influence on you?",
              "Do you think your priorities have changed since you were younger?",
              "What is the most memorable lesson you learned from your parents?",
              "What does success mean to you?",
              "What is the most difficult thing you’ve ever done?",
              "What scares you most about your future?",
              "What keeps you up at night?"]
    await ctx.send(f"Topic:\n {random.choice(starters)}")

@client.command()
async def countdown(ctx, number=3):
    try:
        number=int(number)
        for x in range(number,0,-1):
            await ctx.send(x)
            time.sleep(1)
        await ctx.send("Surprise!")
    except ValueError:
        await ctx.send("The command should be used with a number to countdown from or the default value is 3.")

@client.command()
async def hort(ctx):
    options = ["heads", "tails", "edge"]
    await ctx.send(random.choice(options))

@client.command()
async def randomnumber(ctx, *, limit=10):
    await ctx.send(random.randint(0,limit))


client.remove_command("help")

@client.command()
async def hit(ctx):
    await ctx.send("Watch Yo Profanity!")

@client.command()
async def help(ctx):
    author=ctx.message.author
    commands={"ping":" Returns the latency",
              "8ball":"Returns advice for the question supplied.",
              "spam":"Types an inputted string of text an inputted number of times.",
              "choice":"Chooses an option from a provided list.",
              "clear":"Deletes a specified number of messages",
              "hi":"Sends a friendly greeting",
              "kick":"Kicks a member",
              "ban":"Bans a member",
              "choice":"Chooses an option from a supplied list separated by commas",
              "topic":"Returns a question to start a discussion",
              "roast":"Gives a roast",
              "github":"Sends a link to the source code",
              "hort": "Heads or Tails",
              "randomnumber": "Generate a random-ish number up to the limit specified or (if no limit) 10",
              "ree": "You already know what this does."}
    embed= discord.Embed( colour = discord.Colour.blue())
    embed.set_author(name="Help")
    for x in commands:
        embed.add_field(name=f"${x}", value=commands[x], inline=False)
    await ctx.send(author, embed=embed)

@client.command()
async def roast(ctx):
    roasts=["You’re the reason God created the middle finger.",
            "You’re a grey sprinkle on a rainbow cupcake.",
            "If your brain was dynamite, there wouldn’t be enough to blow your hat off.",
            "You are more disappointing than an unsalted pretzel.",
            "Light travels faster than sound which is why you seemed bright until you spoke.",
            "You're so annoying, you make your Happy Meal cry.",
            "You have so many gaps in your teeth it looks like your tongue is in jail.",
            "Your secrets are always safe with me. I never even listen when you tell me them.",
            "I’ll never forget the first time we met. But I’ll keep trying.",
            "I forgot the world revolves around you. My apologies, how silly of me.",
            "I only take you everywhere I go just so I don’t have to kiss you goodbye.",
            "Hold still. I’m trying to imagine you with personality.",
            "Your face makes onions cry.",
            "It’s impossible to underestimate you.",
            "I’m not a nerd, I’m just smarter than you.",
            "Keep rolling your eyes, you might eventually find a brain.",
            "Your face is just fine but we’ll have to put a bag over that personality.",
            "You bring everyone so much joy, when you leave the room."]
    chosenOne=random.choice(roasts)
    if chosenOne=="You bring everyone so much joy, when you leave the room.":
        chosenOne=chosenOne.split(",")
        for x in chosenOne:
            await ctx.send(x)
            time.sleep(1)
    else:
        await ctx.send(chosenOne)

@client.command()
async def github(ctx):
    await ctx.send("https://github.com/proxamon/proxabot")

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command(aliases=["choose"])
async def choice(ctx,*,string="True"):
    if string=="True":
        await ctx.send("Please enter a list of options after $choice.")
    else:
        if " or " in string:
            string=string.replace(" or ", ",")
        string = string.replace(", ",",")
        options = string.split(",")
        if "anime" in options or "Anime" in options:
            number = random.randint(0,10)
            if number<2:
                await ctx.send("My choice:")
                await ctx.send(random.choice(options).capitalize())
            else:
                await ctx.send("My choice:")
                await ctx.send("Anime")
        else:
            await ctx.send("My choice:")
            await ctx.send(random.choice(options).capitalize())



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
    if ctx.message.author.display_name == "Retr0fade":
        await ctx.send("Hello, creator.")
    else:
        await ctx.send(f'Hello there, {ctx.message.author.display_name}')


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
    await ctx.send(f"Banned {member.name}")

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    flag=False
    if "#" in member:
        bannedPeople=await ctx.guild.bans()
        memberName, memberDiscriminator = member.split("#")

        for banEntry in bannedPeople:
            user=banEntry.user
            if (user.name, user.discriminator)==(memberName, memberDiscriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.name} has been unbanned.")
                flag=True
        if not flag:
            await ctx.send("That person does not exist in the list of banned people.")
    else:
        await ctx.send("Please type the command followed by the username and numberid of the user")
        await ctx.send("For example, $unban person#1234 ")



@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, * , reason = None):
    await member.ban(reason=reason)


client.run(TOKEN)
