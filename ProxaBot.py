import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Create bot instance
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    print(f"Connected to {len(bot.guilds)} guild(s)")
    print("------")

@bot.command(name="hello")
async def hello(ctx):
    """Responds with a hello message that includes the user's name"""
    username = ctx.author.display_name
    await ctx.send(f"hello, {username}")

# Run the bot
def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Error: No Discord token found. Please add your token to a .env file.")
        return
    
    bot.run(token)

if __name__ == "__main__":
    main()