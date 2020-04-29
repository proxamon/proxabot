import discord
from discord.ext import commands

class Games(commands.cog):
    def __init__(self, client):
        self.client=client

    @commands.Cog.listener()


def setup(client):
    client.add_cog(Games(client)):
