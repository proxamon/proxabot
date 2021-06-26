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

    async def updateUserMoney(self, ctx, user, money):
        currency = db.currency
        currentMoney = await self.fetchUserMoney(user)
        currentMoney += money
        currency.delete_one({"user":user.id})
        currency.insert_one({"user":user.id, "money":currentMoney})
        await ctx.send(f"{user.mention}, your current balance is {currentMoney} coins.")

    @commands.command()
    @commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
    async def work(self, ctx):
        pay = random.randint(100, 500)
        await ctx.send("You have worked in the rice fields for 4 hours.")
        await ctx.send(f"Your generous manager paid you {pay} coins")
        await self.updateUserMoney(ctx, ctx.message.author, pay)


    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        if member!=None:
            userBal = await self.fetchUserMoney(member)
            await ctx.send(f"{member.display_name}\'s current balance is {userBal} coins.")
        else:
            userBal = await self.fetchUserMoney(ctx.message.author)
            await ctx.send(f"{ctx.message.author.mention}, your current balance is {userBal} coins.")

        



def setup(client):
    for command in commands.Cog.get_commands(Currency):
        client.remove_command(command.name)
    client.add_cog(Currency(client))
