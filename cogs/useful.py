import discord, random, time, praw, os, requests
from discord.ext import commands
from dotenv import load_dotenv

#Variables to be used in the roast command
#If this pastebin gets taken down or removed, this command will cease to work
roastSource = "https://pastebin.com/raw/HCMHrihv"
roasts = requests.get(roastSource)
listOfRoasts = [m[:-2] for m in roasts.text.split("\n")]

class Useful(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Happy Birthday, I guess?
    @commands.command()
    async def countdown(self, ctx, number=3):
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
    

    #This is for when someone has 0 brain cells, but needs to defend themselves.
    @commands.command()
    async def roast(self, ctx):
        
        chosenOne=random.choice(listOfRoasts)
        await ctx.send(chosenOne)

    #This is... well, you know why I made this.
    @commands.command()
    async def topic(self, ctx):
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
    
    #Lonelyyyyyyy.... I'm Mr Lonellyyyyyy.... I have nobodyyyyyyyy... ooofffff my ooooowwwWWNNNN..
    @commands.command(aliases = ["hello", "Hi", "Hey", "Hello", "hey"])
    async def hi(self, ctx):
        if ctx.message.author.name == "Proxamon":
            await ctx.send("Hello, creator.")
        else:
            await ctx.send(f'Hello there, {ctx.message.author.display_name}')
    
    #Pretty simple, just reverses a string.
    @commands.command()
    async def reverse(self, ctx, *, string):
        await ctx.send(string[::-1])




def setup(client):
    for command in commands.Cog.get_commands(Useful):
        client.remove_command(command.name)
    client.add_cog(Useful(client))