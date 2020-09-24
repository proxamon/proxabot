import discord, random, time, praw, os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
redditClientID=os.getenv("CLIENT_ID")
redditClientSecret=os.getenv("CLIENT_SECRET")
redditUserAgent=os.getenv("USER_AGENT")

#This creates a variable that stores the connection to reddit's API
reddit = praw.Reddit(client_id=redditClientID, client_secret=redditClientSecret, user_agent=redditUserAgent)

class Memes(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Same as @client.command()
    @commands.command()
    async def test(self, ctx):
        await ctx.send("Test successful.")

    #This is a short function to simplify and tidy up the "$meme", "$dankmeme" and "$wholesome" commands
    def fetchMeme(self, ctx, subreddit):
        author=ctx.message.author
        randPost=reddit.subreddit(subreddit).random()
        url=randPost.url
        embed= discord.Embed(colour = discord.Colour.blue())
        embed.set_author(name=f"Meme from r/{subreddit}")
        embed.set_image(url=url)
        return author, embed

    #This is a command to fetch a meme from r/dankmemes
    @commands.command()
    async def dankmeme(self, ctx):
        author, embed = self.fetchMeme(ctx, "dankmemes")
        await ctx.send(author, embed=embed)

    #This is the same as above but for r/wholesomememes
    @commands.command()
    async def wholesome(self, ctx):
        author, embed = self.fetchMeme(ctx, "wholesomememes")
        await ctx.send(author, embed=embed)

    #Same as above but for r/memes
    @commands.command()
    async def meme(self, ctx):
        author, embed = self.fetchMeme(ctx, "memes")
        await ctx.send(author, embed=embed)

def setup(client):
    client.add_cog(Memes(client))