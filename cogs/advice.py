import discord, random, time, praw, os
from discord.ext import commands
from dotenv import load_dotenv

class Advice(commands.Cog):

    def __init__(self, client):
        self.client = client

    #This is for me being a dumb donkey who can't make decisions.
    @commands.command(aliases=["choose"])
    async def choice(self, ctx,*,string="null"):
        if string=="null":
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
    @commands.command(aliases=["8ball", "advice", "chance"])
    async def _8ball(self, ctx, *, question):
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

    #For settling Among Us arguments.
    @commands.command()
    async def hort(self, ctx):
        options = ["heads", "heads","heads","tails", "tails", "tails", "edge"]
        await ctx.send(random.choice(options))

    #This is for when I need a random number and cba to use google.
    @commands.command()
    async def randomnumber(self, ctx, *, limit=10):
        await ctx.send(random.randint(0,limit))       



def setup(client):
    for command in commands.Cog.get_commands(Advice):
        client.remove_command(command.name)
    client.add_cog(Advice(client))