import discord, random, time, praw, pymongo
from discord.ext import commands, tasks
from dotenv import load_dotenv
from os import getenv
import asyncio

load_dotenv()
mongoDBURL = getenv("MONGO_DB_URL")
client = pymongo.MongoClient(mongoDBURL)
db = client.Proxabot
banking = db.banking 

class Banking(commands.Cog):
    def __init__(self, client):
        self.client=client
    
    async def fetchUserBankBal(self, user):
        record = banking.find_one({"user":user.id})
        if record==None:
            banking.insert_one({"user":user.id, "money":0})
            return 0
        return record["money"]

    async def decreaseBankBal(self, ctx, user, amount):
        currentMoney = await self.fetchUserBankBal(user)
        updatedMoney = currentMoney - amount
        banking.update_one({"user":user.id},{"$set":{"money":updatedMoney}})
        await ctx.send(f"{user.display_name}, your current bank balance is {updatedMoney} coins.")

    async def increaseBankBal(self, ctx, user, amount):
        currentMoney = await self.fetchUserBankBal(user)
        updatedMoney = currentMoney + amount
        banking.update_one({"user":user.id},{"$set":{"money":updatedMoney}})
        await ctx.send(f"{user.display_name}, your current bank balance is {updatedMoney} coins.")
    
    @commands.command(aliases = ["with", "wdraw"])
    async def withdraw(self, ctx, amount=None):
        if amount==None:
            await ctx.send("You need to specify how much to withdraw")
            return 

        currency = self.client.get_cog("Currency")
        amount = int(amount)
        bankBal = await self.fetchUserBankBal(ctx.message.author)
        if bankBal>=amount:
            await currency.increaseUserMoney(ctx, ctx.message.author, amount)
            await self.decreaseBankBal(ctx, ctx.message.author, amount)
        else:
            await ctx.send(f"Error! {ctx.message.author.mention}, you do not have that much money.")

    @commands.command()
    async def deposit(self, ctx, amount=None):
        if amount==None:
            await ctx.send("You need to specify how much to deposit")
            return 

        currency = self.client.get_cog("Currency")
        amount = int(amount)
        walletBal = await currency.fetchUserMoney(ctx.message.author)
        if walletBal>=amount:
            await currency.reduceUserMoney(ctx, ctx.message.author, amount)
            await self.increaseBankBal(ctx, ctx.message.author, amount)
        else:
            await ctx.send(f"Error! {ctx.message.author.mention}, you do not have that much money.")



    
        

def setup(client):
    for command in commands.Cog.get_commands(Banking):
        client.remove_command(command.name)
    client.add_cog(Banking(client))
