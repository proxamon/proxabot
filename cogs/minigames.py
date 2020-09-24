import discord, random, time, praw, os
from discord.ext import commands
from dotenv import load_dotenv

class Minigames(commands.Cog):

    def __init__(self, client):
        self.client = client




def setup(client):
    for command in commands.Cog.get_commands(Minigames):
        client.remove_command(command.name)
    client.add_cog(Minigames(client))