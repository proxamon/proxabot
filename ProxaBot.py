import discord, random, time, praw, os
from discord.ext import commands
from dotenv import load_dotenv

#This loads in some secret variables for the connections to discord API and reddit API
load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")
redditClientID=os.getenv("CLIENT_ID")
redditClientSecret=os.getenv("CLIENT_SECRET")
redditUserAgent=os.getenv("USER_AGENT")

#This initialises the bot with the prefix "$"
client=commands.Bot(command_prefix="$")

#This creates a variable that stores the connection to reddit's API
reddit = praw.Reddit(client_id=redditClientID, client_secret=redditClientSecret, user_agent=redditUserAgent)

#This is a class for the muteRole because I was dum when making the mute functions.
class muteRole:
    def __init__(self, id):
        self.id = id

#This is just a short event that runs when the bot connects. It will print out "Bot is ready", for when I'm debugging, and also set its status to "$help"
@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(activity = discord.Game("$help"))

#This is a simple "no u" response function because my sense of comedy as well as my sense of self is slowly deteriorating, please send help.
#I'm just kidding of course.
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

#This is a short function to simplify and tidy up the "$meme", "$dankmeme" and "$wholesome" commands
def fetchMeme(ctx, subreddit):
    author=ctx.message.author
    randPost=reddit.subreddit(subreddit).random()
    url=randPost.url
    embed= discord.Embed(colour = discord.Colour.blue())
    embed.set_author(name=f"Meme from r/{subreddit}")
    embed.set_image(url=url)
    return author, embed

#This is a blocked command I made when I wanted to spam my friend's dms.
#UPDATE: He is not my friend anymore XD
'''@client.command()
async def send_dm(ctx, member: discord.Member):
    channel = await member.create_dm()
    while True:
        await channel.send("This is spam.")'''

#This is a command to fetch a meme from r/dankmemes
@client.command()
async def dankmeme(ctx):
    author, embed = fetchMeme(ctx, "dankmemes")
    await ctx.send(author, embed=embed)

#This is the same as above but for r/wholesomememes
@client.command()
async def wholesome(ctx):
    author, embed = fetchMeme(ctx, "wholesomememes")
    await ctx.send(author, embed=embed)

#Same as above but for r/memes
@client.command()
async def meme(ctx):
    author, embed = fetchMeme(ctx, "memes")
    await ctx.send(author, embed=embed)

#This is a completely dumb command for when someone asks for help.
@client.command()
async def therapy(ctx, member: discord.Member = None):
    if member != None:
        await ctx.send(f"{member.display_name} is beyond even my help.")
    else:
        await ctx.send("You are beyond even my help.")

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

#This command allows me to crusade against someone when they do something unholy.
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

#This was for when I was adding verification to a server and didn't want to go through and manually give everyone the "verified" role.
'''@client.command()
async def massroleassign(ctx):
    if ctx.message.author.name == "Proxamon":
        for member in ctx.guild.members:
            await member.add_roles(discord.utils.get(ctx.guild.roles, name="verified"))'''


#I don't even know what this is for. Also, fun fact: I initially spelt "successful" wrong for this command.
@client.command()
async def test(ctx):
    await ctx.send("Test successful.")

#This command just sends "reee"
@client.command(aliases = ["reeee", "ree", "reeeee"])
async def reee(ctx):
    await ctx.send("REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

#This is a command that has a 20% chance of saving someone
@client.command()
async def save(ctx):
    number = random.randint(0,10)
    if number>8:
        await ctx.send("You have been saved.")
    else:
        await ctx.send("Leave me alone, I have better things to do.")

#This is... well, you know why I made this.
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

#Happy Birthday, I guess?
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

#For settling Among Us arguments.
@client.command()
async def hort(ctx):
    options = ["heads", "tails", "edge"]
    await ctx.send(random.choice(options))

#This is for when I need a random number and cba to use google.
@client.command()
async def randomnumber(ctx, *, limit=10):
    await ctx.send(random.randint(0,limit))

#This allows me to write my own help command.
client.remove_command("help")

#heh.
@client.command()
async def hit(ctx):
    await ctx.send("Watch Yo Profanity!")

#This is a very messy and unorganised implementation of the help command.
#Actually... lemme shift all of this dictionary into a separate file.
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

#This is for when someone has 0 brain cells, but needs to defend themselves.
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

#Always be plugging.
@client.command()
async def github(ctx):
    await ctx.send("https://github.com/proxamon/proxabot")

#Curiosity, I guess...
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

#This is for me being a dumb donkey who can't make decisions.
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


#Same as choice but for advice.
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

#Lonelyyyyyyy.... I'm Mr Lonellyyyyyy.... I have nobodyyyyyyyy... ooofffff my ooooowwwWWNNNN..
@client.command(aliases = ["hello", "Hi", "Hey", "Hello", "hey"])
async def hi(ctx):
    if ctx.message.author.name == "Proxamon":
        await ctx.send("Hello, creator.")
    else:
        await ctx.send(f'Hello there, {ctx.message.author.display_name}')

#This just repeats a message a given number of times, up to 20. For some reason it does it in groups of 5, I don't know.
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

#Pretty simple, just reverses a string.
@client.command()
async def reverse(ctx, *, string):
    await ctx.send(string[::-1])

#Deletes a given number of messages, default 5, maximum 20
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number=5):
    if number<=20:
        await ctx.channel.purge(limit=number+1)
    elif number>20:
        await ctx.send("Maximum 20 messages can be deleted.")
    else:
        await ctx.send("Invalid number of messages.")

#Kicks people.
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, * , reason = None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.name}")

#Unbans people. I don't know why I wrote this before ban but oh well.
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


#Bans people.
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, * , reason = None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.name}")

#Sets a role as the mute role so it can be used later on to mute people.
@client.command(aliases = ["muterole", "setmuterole", "MuteRole"])
async def setMuteRole(ctx, role : discord.Role):

    file = open("botData/muteRoles.txt", "r")
    lines = file.readlines()
    file.close()

    file = open("botData/muteRoles.txt", "w")
    for x in range(len(lines)):
        try:
            if (lines[x].strip().split(":"))[0]==str(ctx.guild.id):
                del lines[x]
        except:
            pass
    for line in lines:
        file.write(line)
    file.close()

    file=open("botData/muteRoles.txt", "a")
    file.write(f"{ctx.guild.id}:{role.id}\n")
    file.close()

    await ctx.send(f"Set Mute Role to {role.mention}")

#Assigns the aforementioned mute role to someone, to mute them.
@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member : discord.Member, *, reason = "LUL"):
    file = open("botData/muteRoles.txt", "r")
    for line in file:
        guildID, roleID = line.strip().split(":")
        if guildID==str(ctx.guild.id):
            muteRole1=muteRole(roleID)
            break
    file.close()
    try:
        await member.add_roles(muteRole1)
        await ctx.send(f"Muted {member.mention}")
    except UnboundLocalError:
        await ctx.send(f"Sorry, you have not set a mute role yet.")
        await ctx.send("Please set a role through $muterole <mentionTheRoleHere>")
    
#Removes the mute role from someone.
@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member : discord.Member, *, reason = "LUL"):
    file = open("botData/muteRoles.txt", "r")
    for line in file:
        guildID, roleID = line.strip().split(":")
        print(guildID)
        print(roleID)
        if guildID==str(ctx.guild.id):
            muteRole1=muteRole(roleID)
            break
    file.close()
    try:
        await member.remove_roles(muteRole1)
        await ctx.send(f"Unmuted {member.mention}")
    except UnboundLocalError:
        await ctx.send(f"Sorry, you have not set a mute role yet.")
        await ctx.send("Please set a role through $muterole <mentionTheRoleHere>")


client.run(TOKEN)
