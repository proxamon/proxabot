import discord, random, time, praw, pymongo
from os import getenv
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
mongoDBURL = getenv("MONGO_DB_URL")
client = pymongo.MongoClient(mongoDBURL)
db = client.Proxabot


#This is a class for the muteRole because I was dum when making the mute functions.
class muteRole:
    def __init__(self, id):
        self.id = id

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def fetchMuteRole(self, ctx, guildID):
        muteRoles = db.muteRoles
        record = muteRoles.find_one({"guild":ctx.guild.id})
        if record==None:
            await ctx.send(f"Sorry, you have not set a mute role yet.")
            await ctx.send("Please set a role through $muterole <mentionTheRoleHere>")
            return None
        return muteRole(record["role"])


    #Bans people.
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, * , reason = None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.name}")

    #Unbans people. I don't know why I wrote this before ban but oh well.
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        flag=False
        if "#" in member:
            bannedPeople=await ctx.guild.bans()
            memberName, memberDiscriminator = member.split("#")

            for banEntry in bannedPeople:
                user=banEntry.user
                if (user.name, user.discriminator)==(memberName, memberDiscriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f"{user.name} has been unbanned.")
                    flag=True
            if not flag:
                await ctx.send("That person does not exist in the list of banned people.")
        else:
            await ctx.send("Please type the command followed by the username and numberid of the user")
            await ctx.send("For example, $unban person#1234 ")

    #Sets a role as the mute role so it can be used later on to mute people.
    @commands.command(aliases = ["muterole", "setmuterole", "MuteRole"])
    async def setMuteRole(self, ctx, role : discord.Role):

        muteRoles = db.muteRoles
        muteRoles.delete_one({"guild":ctx.guild.id})
        muteRoles.insert_one({"guild":ctx.guild.id, "role":role.id})

        await ctx.send(f"Set Mute Role to {role.mention}")

    #Assigns the aforementioned mute role to someone, to mute them.
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member : discord.Member, *, reason = "LUL"):

        muteRole1 = await self.fetchMuteRole(ctx, ctx.guild.id)

        if muteRole1==None:
            return

        try:
            await member.add_roles(muteRole1)
            await ctx.send(f"Muted {member.mention}")
            
        except Exception as e:
            await ctx.send(e)


    #Removes the mute role from someone.
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member : discord.Member, *, reason = "LUL"):
        muteRole1 = await self.fetchMuteRole(ctx, ctx.guild.id)

        if muteRole1==None:
            return

        try:
            await member.remove_roles(muteRole1)
            await ctx.send(f"Unmuted {member.mention}")
        except Exception as e:
            await ctx.send(e)

    #Deletes a given number of messages, default 5, maximum 20
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, number=5):
        if number<=20:
            await ctx.channel.purge(limit=number+1)
        elif number>20:
            await ctx.send("Maximum 20 messages can be deleted.")
        else:
            await ctx.send("Invalid number of messages.")

    #Kicks people.
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, * , reason = None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.name}")

    #Curiosity, I guess...
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

def setup(client):
    for command in commands.Cog.get_commands(Admin):
        client.remove_command(command.name)
    client.add_cog(Admin(client))