import discord, random, time, os
import asyncpraw as praw
from discord.ext import commands
from dotenv import load_dotenv
from prawcore.exceptions import NotFound

load_dotenv()
redditClientID=os.getenv("CLIENT_ID")
redditClientSecret=os.getenv("CLIENT_SECRET")
redditUserAgent=os.getenv("USER_AGENT")

#This creates a variable that stores the connection to reddit's API
reddit = praw.Reddit(client_id=redditClientID, client_secret=redditClientSecret, user_agent=redditUserAgent)

class Reddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Same as @client.command()
    @commands.command()
    async def test(self, ctx):
        await ctx.send("Test successful.")

    #This is a short function to simplify and tidy up the "$meme", "$dankmeme" and "$wholesome" commands
    async def fetchMeme(self, ctx, subreddit, attempts=1):
        subredditObj = await reddit.subreddit(subreddit)
        randPost = await subredditObj.random()
        if not randPost.over_18:
            postAuthor = randPost.author.name
            postUpvotes = randPost.score
            postTitle = randPost.title
            url=randPost.url
            footer = postUpvotes
            print(randPost.post_hint)
            redditUpvote = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn130.picsart.com%2F304352163103211.png&f=1&nofb=1"

            if randPost.is_self:
                embed = discord.Embed(colour = discord.Colour.blue(), title = postTitle, description = randPost.selftext)
            elif randPost.is_video or randPost.post_hint in ["gallery", "rich:video"]:
                print("video detected")
                if attempts==5:
                    print("Should be error message")
                    embed = discord.Embed(colour = discord.Colour.red(), description = "I could only find videos, which are not currently supported.")
                    attempts=0
                    return await ctx.send(embed=embed)
                attempts+=1
                print("finding new result")
                await self.fetchMeme(ctx, subreddit, attempts)
                print("found new result")
                
            else:
                embed= discord.Embed(colour = discord.Colour.blue(), title = postTitle)
                embed.set_image(url=url)

            embed.set_author(name=postAuthor)            
            embed.set_footer(text=footer, icon_url=redditUpvote)
            return embed
        else:
            embed= discord.Embed(colour = discord.Colour.red(), description = "That is NSFW which is not permitted.")
            return embed
            

    #This is a command to fetch a meme from r/dankmemes
    @commands.command()
    async def dankmeme(self, ctx):
        embed = await self.fetchMeme(ctx, "dankmemes")
        await ctx.send(embed=embed)

    #This is the same as above but for r/wholesomememes
    @commands.command()
    async def wholesome(self, ctx):
        embed = await self.fetchMeme(ctx, "wholesomememes")
        await ctx.send(embed=embed)

    #Same as above but for r/memes
    @commands.command()
    async def meme(self, ctx):
        embed = await self.fetchMeme(ctx, "memes")
        await ctx.send(embed=embed)

    @commands.command()
    async def eyebleach(self, ctx):
        embed = await self.fetchMeme(ctx, "eyebleach")
        await ctx.send(embed=embed)

    @commands.command()
    async def animals(self, ctx):
        animalSubreddits = ["aww", "sneks", "rarepuppers", "pigtures", "wildlifephotography"]
        embed = await self.fetchMeme(ctx, random.choice(animalSubreddits))
        await ctx.send(embed=embed)
        
    @commands.command(aliases=["nuggets", "nugget", "nuggie"])
    async def nuggies(self, ctx):
        embed = await self.fetchMeme(ctx, "chickennuggets")
        await ctx.send(embed=embed)


    @commands.command()
    async def redditfetch(self, ctx, subreddit=None):
        if subreddit!=None:
            try:
                subreddit=subreddit.strip("r/")
                embed = await self.fetchMeme(ctx, subreddit)
                await ctx.send(embed=embed)
            except NotFound:
                await ctx.send("That subreddit does not exist.")
        else:
            await ctx.send("Please provide a subreddit as a parameter")
            await ctx.send("For example: $redditFetch r/programminghorror")

def setup(client):
    client.add_cog(Reddit(client))
