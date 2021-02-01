import discord, random, time, praw, os, asyncio
from discord.ext import commands
from dotenv import load_dotenv

class Money(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["bal", "money", "balanse"])
    async def balance(self, ctx):
        logData = []
        logs = open("botData/currency.txt", "r")
        for line in logs:
            '''if (line.strip().split(":"))[0] == message.author.id:
                plrTotal = (line.strip().split(":"))[1]
                found = True
            logData.append(line)'''

            logData.append(line.strip().split(":"))
        logs.close()
        
        for person in logData:
            if int(person[0])==ctx.message.author.id:
                await ctx.send(f"{ctx.message.author.mention} Your balance: {person[1]}")
                break


def setup(client):
    for command in commands.Cog.get_commands(Money):
        client.remove_command(command.name)
    client.add_cog(Money(client))