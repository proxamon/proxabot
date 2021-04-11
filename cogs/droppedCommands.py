import discord, random, time, praw, os
from discord.ext import commands
from dotenv import load_dotenv

class DropCmds(commands.Cog):

    def __init__(self, client):
        self.client = client


    #This is a blocked command I made when I wanted to spam my friend's dms.
    #UPDATE: He is not my friend anymore 
    '''@commands.command()
    async def send_dm(ctx, member: discord.Member):
        channel = await member.create_dm()
        while True:
            await channel.send("This is spam.")'''

    #This was for when I was adding verification to a server and didn't want to go through and manually give everyone the "verified" role.
    '''@commands.command()
    async def massroleassign(ctx):
        if ctx.message.author.name == "Proxamon":
            for member in ctx.guild.members:
                await member.add_roles(discord.utils.get(ctx.guild.roles, name="verified"))'''

    #I don't even know what this is for. Also, fun fact: I initially spelt "successful" wrong for this command.
    '''@commands.command()
    async def test(ctx):
        await ctx.send("Test successful.")'''


def setup(client):
    for command in commands.Cog.get_commands(DropCmds):
        client.remove_command(command.name)
    client.add_cog(DropCmds(client))