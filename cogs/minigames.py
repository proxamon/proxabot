import discord, random, time, praw, os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

class Minigames(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.amogusEmojiIDs = [862406483140542474,
                               862406483140542474,
                               862406483140542474,
                               862406483140542474,
                               862406524415770624,
                               862406555827437598,
                               862406583865966612,
                               862406609123541002,
                               862406646605283338,
                               862406673371889688,
                               862406700224217149,
                               862406721259831326,
                               862406743224877056,
                               862406772613447691,
                               862406816683786271]

    @commands.command()
    async def guess(self, ctx, countdown=5, randomNum=0):
        currency = client.get_cog("Currency")
        

        if countdown==5:
            randomNum = random.randint(1,20)
            await ctx.send("I have chosen a random number between 1 and 20 (inclusive).")
            await ctx.send("You have 5 tries to guess it.")
        try:
            attempt = await self.client.wait_for("message", check=lambda message: message.author==ctx.message.author and message.content.isdigit(), timeout=30.0)
        except asyncio.TimeoutError:
            return await ctx.send(f"Timed out. The answer was {randomNum}")
        
        if int(attempt.content)==randomNum:
            await ctx.send(f"Good job, you got it in {6-countdown} tries! :D ")
            winnings = random.randint(1, 2000)
            await currency.increaseUserMoney(ctx, ctx.message.author, winnings)
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


    @commands.command()
    async def roulette(self, ctx, amount=1):
        currency = self.client.get_cog("Currency")
        rouletteWheel=""
        usrBal = await currency.fetchUserMoney(ctx.message.author)
        if usrBal<amount:
            return await ctx.send("You can't bet that much!")

        if amount<0:
            return await ctx.send("You can't bet negative amounts!")

        failureID = 862406483140542474 #ID of red impostor 
        emojis = self.amogusEmojiIDs
        random.shuffle(emojis)
        chosenFive = emojis[0:5]
        result = chosenFive[2]
        if result == failureID:
            colour = discord.Colour.red()
            await currency.reduceUserMoney(ctx, ctx.message.author, amount, True)
            message = f"You got the red impostor! Your result was SUS! You lose {amount} coins."
        else:
            colour = discord.Colour.green()
            amount = amount//4
            await currency.increaseUserMoney(ctx,ctx.message.author, amount, True)
            message = f"You got a crewmate! You won {amount} coins."


        embed = discord.Embed(colour = colour)
        embed.title = "Amogus roulette"
        embed.add_field(name="\u200b", value="The middle crewmate is your result.", inline=False)
        for emojiID in chosenFive:
            emoji = self.client.get_emoji(emojiID)
            #embed.add_field(name="\u200b",value=self.client.get_emoji(emojiID),  inline=True)
            rouletteWheel+=f"{str(emoji)}"
            rouletteWheel+="\t"
        embed.add_field(name='\u200b', value=rouletteWheel, inline=False)
        embed.add_field(name="\u200b",value=message,  inline=False)
        await ctx.send(embed=embed)
   
    @commands.command()
    async def lottery(self, ctx):
        ticketCost = 500
        winnings = 1000000
        currency = self.client.get_cog("Currency")
        didReduce = await currency.reduceUserMoney(ctx, ctx.message.author, ticketCost, True)
        if not didReduce:
            await ctx.send("A ticket costs {ticketCost} amoguscoins")
            return
        if random.randint(1,100)==69:
            await currency.increaseUserMoney(ctx, ctx.message.author, winnings+ticketCost, True)
            embed = discord.Embed(colour=discord.Colour.green())
            message = f"You won! You win {winnings} amoguscoins"
        else:
            embed = discord.Embed(colour=discord.Colour.red())
            message = "You didn't win anything... this time. Better luck next time :)"
        embed.title="Lottery Results"
        embed.add_field(name="\u200b",value=message,  inline=False)
        await ctx.send(embed=embed)
        

def setup(client):
    for command in commands.Cog.get_commands(Minigames):
        client.remove_command(command.name)
    client.add_cog(Minigames(client))
