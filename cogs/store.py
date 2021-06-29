import discord, random, time, praw, pymongo
from discord.ext import commands, tasks
from dotenv import load_dotenv
from os import getenv
from collections import Counter
import asyncio

load_dotenv()
mongoDBURL = getenv("MONGO_DB_URL")
client = pymongo.MongoClient(mongoDBURL)
db = client.Proxabot
shop = db.shop
inventories = db.inventories


class Store(commands.Cog):
    def __init__(self, client):
        self.client=client

    async def genInvEmbed(self, user):
        userData = inventories.find_one({"user":user.id})
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.title="Inventory"
        if userData is None:
            return embed
        items = Counter(list(userData["inventory"]))
        for item, number in items.items():
            embed.add_field(name=item, value=number, inline=False)
        return embed
    
    async def updateUserInventory(self, user, item, mode="addition"):
        currentUserInventory = list(inventories.find_one({"user":user.id})["inventory"])
        if mode=="addition":
            currentUserInventory.append(item)
        else:
            if item not in currentUserInventory:
                return False
            currentUserInventory.remove(item)
        inventories.update_one({"user":user.id},{"$set":{"inventory":currentUserInventory}})

    @commands.command(aliases = ["purchase"])
    async def buy(self, ctx, *, itemName):
        user = ctx.message.author
        currency = self.client.get_cog("Currency")
        itemDetails = shop.find_one({"name":itemName.capitalize()})
        didReduce = await currency.reduceUserMoney(ctx, user, int(itemDetails["price"]))
        if not didReduce:
            return
        await self.updateUserInventory(user, itemName.capitalize(), "addition")
        embed = await self.genInvEmbed(user)
        await ctx.send(f"{user.display_name}, your updated inventory:")
        await ctx.send(embed=embed)




    
    @commands.command(aliases=["inv","items","stuff"])
    async def inventory(self, ctx):
        embed = await self.genInvEmbed(ctx.message.author)
        await ctx.send(embed = embed)



def setup(client):
    for command in commands.Cog.get_commands(Store):
        client.remove_command(command.name)
    client.add_cog(Store(client))