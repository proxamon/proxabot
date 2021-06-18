import discord, random, time, praw, os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

class Minigames(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def guess(self, ctx, countdown=5, randomNum=0):
        

        if countdown==5:
            randomNum = random.randint(1,20)
            await ctx.send("I have chosen a random number between 1 and 20 (inclusive).")
            await ctx.send("You have 5 tries to guess it.")
        try:
            attempt = await self.client.wait_for("message", check=lambda message: message.author==ctx.author and message.content.isdigit(), timeout=30.0)
        except asyncio.TimeoutError:
            return await ctx.send(f"Timed out. The answer was {randomNum}")
        
        if int(attempt.content)==randomNum:
            await ctx.send(f"Good job, you got it in {6-countdown} tries! :D ")
        else:
            await ctx.send("Unfortunately, you did not get it correct.")
            if max(randomNum, int(attempt.content))==randomNum:
                await ctx.send("Your number is too low")
            else:
                await ctx.send("Your number is too high")
            await ctx.send(f"You have {countdown-1} tries left.")
            countdown-=1
            if countdown==0:
                return await ctx.send(f"You have run out of tries. The number was {randomNum}")
            await self.guess(ctx, countdown, randomNum)






def setup(client):
    for command in commands.Cog.get_commands(Minigames):
        client.remove_command(command.name)
    client.add_cog(Minigames(client))