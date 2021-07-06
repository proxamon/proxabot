import discord, random, time, praw, pymongo, string
from discord.ext import commands, tasks
from dotenv import load_dotenv
from os import getenv
from collections import Counter
import asyncio

load_dotenv()
mongoDBURL = getenv("MONGO_DB_URL")
botOwnerID = getenv("BOT_OWNER_ID")
client = pymongo.MongoClient(mongoDBURL)
db = client.Proxabot
shop = db.shop
inventories = db.inventories

class Store(commands.Cog):
    def __init__(self, client):
        self.client=client

    async def genBodyPillowList(self, user):
        pillowList=[]
        userData = inventories.find_one({"user":user.id})
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.title="Pillows"
        if userData is None:
            return embed
        invList = list(userData["inventory"])
        for item in invList:
            if item.__contains__("body pillow"):
                pillowList.append(item)
        for i in range(len(pillowList)):
            embed.add_field(name=pillowList[i+1], value=f"Pillow #{i}", inline=False)
        return embed
        


    async def genInvEmbed(self, user):
        userData = inventories.find_one({"user":user.id})
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.title="Inventory"
        if userData is None:
            return embed
        invList = list(userData["inventory"])
        for i in range(len(invList)):
            if "body pillow" in invList[i]:
                invList[i]="Body Pillow"
        items = Counter(invList)
        for item, number in items.items():
            embed.add_field(name=item, value=number, inline=False)
        return embed
    
    async def updateUserInventory(self, user, item, mode="addition"):
        currentUserInventory = inventories.find_one({"user":user.id})
        if currentUserInventory == None:
            inventories.insert_one({"user":user.id, "inventory":[]})
            currentUserInventory = list(inventories.find_one({"user":user.id})["inventory"])
        else:
            currentUserInventory = list(currentUserInventory["inventory"])
        if mode=="addition":
            currentUserInventory.append(item)
        else:
            if item not in currentUserInventory:
                return False
            currentUserInventory.remove(item)
        inventories.update_one({"user":user.id},{"$set":{"inventory":currentUserInventory}})
        return True

    @commands.command(aliases = ["purchase"])
    async def buy(self, ctx, *, itemName):
        user = ctx.message.author
        botOwner = await self.client.fetch_user(int(botOwnerID))
        currency = self.client.get_cog("Currency")
        itemDetails = shop.find_one({"name":string.capwords(itemName)})


        if itemName.lower()=="body pillow":
            try:
                await ctx.send("Please send the name of the waifu/husbando of whom you would like this pillow to be: ")
                attempt = await self.client.wait_for("message", check=lambda message: message.author==user, timeout=30.0)
                itemName = f"{string.capwords(attempt.content)} Body Pillow"
            except asyncio.TimeoutError:
                return await ctx.send("No name specified, forfeiting purchase.")

        didReduce = await currency.reduceUserMoney(ctx, user, int(itemDetails["price"]))
        if not didReduce:
            return
        
        await self.updateUserInventory(user, itemName.capitalize(), "addition")
        await currency.increaseUserMoney(ctx, botOwner, int(itemDetails["price"]), silent=True)
        embed = await self.genInvEmbed(user)
        await ctx.send(f"{user.display_name}, your updated inventory:")
        await ctx.send(embed=embed)

    @commands.command(aliases=["shop"])
    async def store(self, ctx):
        shopItems = shop.find()
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.title="Shop"
        for item in shopItems:
            embed.add_field(name=item["name"],value=f"{item['price']} amoguscoins", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def sell(self, ctx, itemName):
        user = ctx.message.author
        currency = self.client.get_cog("Currency")
        itemDetails = shop.find_one({"name":string.capwords(itemName)})
        didSell = await self.updateUserInventory(user, itemName.capitalize(), "subtraction")
        if not didSell:
            await ctx.send("You do not own that item")
            return
        embed = await self.genInvEmbed(user)
        await currency.increaseUserMoney(ctx, user, int(itemDetails["price"]))
        await ctx.send(f"{user.display_name}, your updated inventory:")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["inv","items","stuff"])
    async def inventory(self, ctx, member: discord.Member = None):
        if member==None:
            embed = await self.genInvEmbed(ctx.message.author)
        else:
            embed = await self.genInvEmbed(member)
        await ctx.send(embed = embed)

    @commands.command(aliases=["pillows", "bodypillows", "bodypillow"])
    async def bodyPillows(self, ctx, member: discord.Member = None):
        if member==None:
            embed = await self.genBodyPillowList(ctx.message.author)
        else:
            embed = await self.genBodyPillowList(member)
        await ctx.send(embed=embed)




def setup(client):
    for command in commands.Cog.get_commands(Store):
        client.remove_command(command.name)
    client.add_cog(Store(client))
