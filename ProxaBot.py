import discord
import random
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
import praw

load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")
redditClientID=os.getenv("CLIENT_ID")
redditClientSecret=os.getenv("CLIENT_SECRET")
redditUserAgent=os.getenv("USER_AGENT")
muteRole = ""

client=commands.Bot(command_prefix="$")

reddit = praw.Reddit(client_id=redditClientID, client_secret=redditClientSecret, user_agent=redditUserAgent)

print(reddit.read_only)

@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(activity = discord.Game("$help"))

@client.event
async def on_message(message):
    responses1=["Still you","https://www.youtube.com/watch?v=TyfNZs2dPto",
                "ur dad", "It's not me, it's youuuuu.", "no u.", "uno reverse",
                "ur face", "don't be a cuck", "undoubtedly u" ]
    responses2=["The pleasure's all mine.", "No problem!",
                "You are very welcome.", "At least someone says thank you.",
                "Your gratitude is much appreciated.", "There's no need to thank me."]
    if ("no u " in str(message.content.lower()) and not(message.author == client.user)) or (str(message.content.lower())=="no u"):
        reply=random.choice(responses1)
        await message.channel.send(reply)
    #elif "thank" in str(message.content.lower()) and not(message.author == client.user):
        #reply=random.choice(responses2)
        #await message.channel.send(reply)
    #if random.randint(0, 10)==7:
    #    await message.channel.send("Pokemon Spawned")
    #if message.author.id==284738961631608832 and random.randint(1, 100)>65:
        # await message.channel.send(message.content)

    await client.process_commands(message)

def fetchMeme(ctx, subreddit):
    author=ctx.message.author
    randPost=reddit.subreddit(subreddit).random()
    url=randPost.url
    embed= discord.Embed(colour = discord.Colour.blue())
    embed.set_author(name=f"Meme from r/{subreddit}")
    embed.set_image(url=url)
    return author, embed

'''@client.command()
async def send_dm(ctx, member: discord.Member):
    channel = await member.create_dm()
    while True:
        await channel.send("This is spam.")'''

@client.command()
async def dankmeme(ctx):
    author, embed = fetchMeme(ctx, "dankmemes")
    await ctx.send(author, embed=embed)

@client.command()
async def wholesome(ctx):
    author, embed = fetchMeme(ctx, "wholesomememes")
    await ctx.send(author, embed=embed)

@client.command()
async def meme(ctx):
    author, embed = fetchMeme(ctx, "memes")
    await ctx.send(author, embed=embed)

@client.command()
async def therapy(ctx, member: discord.Member = None):
    if member != None:
        await ctx.send(f"{member.display_name} is beyond even my help.")
    else:
        await ctx.send("You are beyond even my help.")

@client.command()
async def join(ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command()
async def crusade(ctx, member: discord.Member = None):
    bibleVerses = ["Again Jesus said, 'Peace be with you! As the Father has sent me, I am sending you.'",
                   "We are witnesses of these things, and so is the Holy Spirit, whom God has given to those who obey him.",
                   "Therefore, my dear brothers and sisters, stand firm. Let nothing move you. Always give yourselves fully to the work of the Lord, because you know that your labor in the Lord is not in vain.",
                   "It is the Lord your God you must follow, and him you must revere. Keep his commands and obey him; serve him and hold fast to him.",
                   "In the same way, the Spirit helps us in our weakness. We do not know what we ought to pray for, but the Spirit himself intercedes for us through wordless groans.",
                   "Come near to God and he will come near to you. Wash your hands, you sinners, and purify your hearts, you double-minded.",
                   "But when you ask, you must believe and not doubt, because the one who doubts is like a wave of the sea, blown and tossed by the wind.",
                   "Surely God is my help; the Lord is the one who sustains me.", "Keep this Book of the Law always on your lips; meditate on it day and night, so that you may be careful to do everything written in it. Then you will be prosperous and successful.",
                   "For he is God's servant for your good. But if you do wrong, be afraid, for he does not bear the sword in vain. For he is the servant of God, an avenger who carries out God's wrath on the wrongdoer.",
                   "But as for these enemies of mine, who did not want me to reign over them, bring them here and slaughter them before me."]
    if member!=None:
        await ctx.send("Opening Bible...")
        time.sleep(0.5)
        verse=random.choice(bibleVerses)
        await ctx.send(f"'{verse}'")
        await ctx.send("Amen.")
        time.sleep(1)
        await ctx.send(f"Now, onwards, my brethren, let us charge with the spirit of God against the satan-spawn that is {member.name}!")
        time.sleep(0.5)
        await ctx.send("HUZZAH!")
    else:
        await ctx.send("Brethren, we cannot crusade without a foe. That would be against the will of God.")

'''@client.command()
async def massroleassign(ctx):
    if ctx.message.author.name == "Proxamon":
        for member in ctx.guild.members:
            await member.add_roles(discord.utils.get(ctx.guild.roles, name="verified"))'''



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
        if number<60:
            number=int(number)
            for x in range(number,0,-1):
                await ctx.send(x)
                time.sleep(1)
            await ctx.send("Surprise!")
        else:
            await ctx.send("The maximum is 60.")
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
              "ree": "You already know what this does.",
              "therapy": "Grants **amazing** therapy to anyone mentioned or the sender, if no one is mentioned.",
              "crusade": "Crusades against a mentioned foe of God.",
              "muterole": "Sets the mentioned role as the role to be assigned when someone is muted.",
              "mute": "Assigns the \"mute\" role to a mentioned person",
              "unmute": "Removes the \"mute\" role from a mentioned person."}
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
    if ctx.message.author.name == "Proxamon":
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
async def reverse(ctx, *, string):
    await ctx.send(string[::-1])

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
    await ctx.send(f"Kicked {member.name}")


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
    await ctx.send(f"Banned {member.name}")

@client.command(aliases = ["muterole", "setmuterole", "MuteRole"])
async def setMuteRole(ctx, role : discord.Role):
    global muteRole
    muteRole = role
    await ctx.send(f"Set Mute Role to {role.mention}")

@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member : discord.Member, *, reason = "LUL"):
    await member.add_roles(muteRole)
    await ctx.send(f"Muted {member.mention}")

@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member : discord.Member, *, reason = "LUL"):
    await member.remove_roles(muteRole)
    await ctx.send(f"Unmuted {member.mention}")



client.run(TOKEN)
