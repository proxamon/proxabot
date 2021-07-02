import discord, random, time, praw, pymongo
from discord.ext import commands, tasks
from dotenv import load_dotenv
from os import getenv
import asyncio

load_dotenv()
mongoDBURL = getenv("MONGO_DB_URL")
client = pymongo.MongoClient(mongoDBURL)
db = client.Proxabot

class Currency(commands.Cog):
    def __init__(self, client):
        self.client=client

    async def fetchUserMoney(self, user):
        currency = db.currency
        record = currency.find_one({"user":user.id})
        if record==None:
            currency.insert_one({"user":user.id, "money":0})
            return 0
        return record["money"]

    async def increaseUserMoney(self, ctx, user, money):
        currency = db.currency
        currentMoney = await self.fetchUserMoney(user)
        currentMoney += money
        currency.update_one({"user":user.id},{"$set":{"money":currentMoney}})
        await ctx.send(f"{user.display_name}, your current balance is {currentMoney} coins.")
    
    async def reduceUserMoney(self, ctx, user, payment):
        currency = db.currency 
        currentMoney = await self.fetchUserMoney(user)
        if payment>currentMoney:
            await ctx.send("You can't spend that much money!")
            return False
        updatedMoney = currentMoney - payment
        currency.update_one({"user":user.id},{"$set":{"money":updatedMoney}})
        await ctx.send(f"{user.display_name}, your current balance is {updatedMoney} coins.")
        return True

    @commands.command()
    @commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
    async def work(self, ctx):
        pay = random.randint(100, 500)
        await ctx.send("You have worked in the rice fields for 4 hours.")
        await ctx.send(f"Your generous manager paid you {pay} coins")
        await self.increaseUserMoney(ctx, ctx.message.author, pay)

    @commands.command()
    async def send(self, ctx, recipient: discord.Member=None, money=None):
        if recipient==None or type(recipient) is int or money==None:
            await ctx.send("There was an error.")
            await ctx.send("Please format the message as follows: ")
            await ctx.send("$send <@recipient> <amount>")
            await ctx.send("For example, $send @Proxamon 8923")
            return
        money = int(money)
        sender = ctx.message.author
        balCheck = await self.reduceUserMoney(ctx, sender, money)
        if balCheck:
            await self.increaseUserMoney(ctx, recipient, money)
        else:
            return

    @commands.command(aliases=["lb", "rich", "lboard"])
    async def leaderboard(self, ctx):
        currency = db.currency
        players = currency.find(sort=[("money", pymongo.DESCENDING)], limit=5)
        counter=1
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name="Leaderboard")   
        for player in players:
            playerObject = await self.client.fetch_user(player["user"])
            username = playerObject.name 
            balance = player["money"]
            embed.add_field(name=f"{counter}) {username}", value=f"Balance: {balance}", inline=False)
            counter+=1
        await ctx.send(embed=embed)

    @commands.command(aliases=["bal", "wallet"])
    async def balance(self, ctx, member: discord.Member = None):
        banking = self.client.get_cog("Banking")
        if member!=None:
            userBal = await self.fetchUserMoney(member)
            bankBal = await banking.fetchUserBankBal(member)
            await ctx.send(f"{member.display_name}\'s current balance is {userBal} amoguscoins.")
            await ctx.send(f"{member.display_name}\'s current bank balance is {bankBal} amoguscoins.")
        else:
            userBal = await self.fetchUserMoney(ctx.message.author)
            bankBal = await banking.fetchUserBankBal(ctx.message.author)
            await ctx.send(f"{ctx.message.author.display_name}, your current balance is {userBal} amoguscoins.")
            await ctx.send(f"{ctx.message.author.display_name}\'s current bank balance is {bankBal} amoguscoins.")

def setup(client):
    for command in commands.Cog.get_commands(Currency):
        client.remove_command(command.name)
    client.add_cog(Currency(client))
