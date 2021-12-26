import discord, random, time, praw, os, pymongo
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()
mongoDBURL = os.getenv("MONGO_DB_URL")
dbClient = pymongo.MongoClient(mongoDBURL)
db = dbClient.Proxabot

class Minigames(commands.Cog):

    def __init__(self, client):
        self.client = client

    #This command allows me to crusade against someone when they do something unholy.
    @commands.command()
    async def crusade(self, ctx, member: discord.Member = None):
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

    #This command just sends "reee"
    @commands.command(aliases = ["reeee", "ree", "reeeee"])
    async def reee(self, ctx):
        await ctx.send("REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

    #This is a command that has a 20% chance of saving someone
    @commands.command()
    async def save(self, ctx):
        number = random.randint(0,10)
        if number>8:
            await ctx.send("You have been saved.")
        else:
            await ctx.send("Leave me alone, I have better things to do.")
    
    #This just repeats a message a given number of times, up to 20. For some reason it does it in groups of 5, I don't know.
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def spam(self, ctx,*,string):
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

    #This is a completely dumb command for when someone asks for help.
    @commands.command()
    async def therapy(self, ctx, member: discord.Member = None):
        if member != None:
            await ctx.send(f"{member.display_name} is beyond even my help.")
        else:
            await ctx.send("You are beyond even my help.")

    #heh.
    @commands.command()
    async def hit(self, ctx):
        await ctx.send("Watch Yo Profanity!")

    @commands.command()
    async def nut(self, ctx):
        await ctx.send("nut")

    @commands.command()
    async def quote(self, ctx, quote= None):
        quotes= db.quotes

        if quote==None:
            await ctx.send("Use of command invalid.")
            await ctx.send("$quote @user - This will fetch the quote (if available) of the mentioned user.")
            await ctx.send("$quote {message URL} - This will change the quote of the message author to the linked quote")
            await ctx.send("Ensure message URL is a valid URL")
            return
        
        msg = None
        if "<" in quote: 
            memberID = quote[3:-1]
            member = await self.client.fetch_user(memberID)
            userData = quotes.find_one({"user":member.id})
            if userData==None:
                await ctx.send("There is no quote for this user")
            else:
                quote = userData["quote"]
                await ctx.send(f"\"{quote}\" - {member.display_name}")
            return
        else:
            msg = quote
            member = None

        linkSects = msg.split("/")
        guild = int(linkSects[-3])
        channel = int(linkSects[-2])
        message = int(linkSects[-1])
        msgText = await self.client.get_guild(guild).get_channel(channel).fetch_message(message)
        author = msgText.author
        msg = msgText.content
        userData = quotes.find_one({"user":author.id})

        if userData==None:
            quotes.insert_one({"user":author.id, "quote":msg})
        else:
            quotes.update_one({"user":author.id},{"$set":{"quote":msg}})

        await ctx.send(f"{author.display_name}'s quote has been updated")
            

    @commands.command()
    async def xkcd(self, ctx, number=None):
        if number==None:
            limit = requests.get("https://xkcd.com/info.0.json").json()["num"]
            number = random.randint(1, limit)
        result = requests.get(f"https://xkcd.com/{number}/info.0.json")
        if result.status_code == 404:
            await ctx.send("Invalid xkcd number!")
            return
        result = result.json()
        embed = discord.Embed(colour = discord.Colour.blue())
        embed.title = result["safe_title"]
        embed.set_image(url=result["img"])
        embed.set_footer(text=result["alt"])
        await ctx.send(embed=embed)

def setup(client):
    for command in commands.Cog.get_commands(Minigames):
        client.remove_command(command.name)
    client.add_cog(Minigames(client))
