import discord
from discord.ext import commands
from discord.utils import get, find
import asyncio
import datetime
from datetime import datetime
import os
import requests
import json

import keep_alive
keep_alive.keep_alive()

color = 0x2f3136



intents = discord.Intents.default()
intents.members = True
intents.guilds = True

def get_prefix(client, message):

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes.get(str(message.guild.id), "-")


client = commands.Bot(command_prefix=get_prefix,
                      case_insensitive=True,
                      intents=intents)
client.remove_command("help")


## --------------------------------- ##
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')
#####------------\!/--------------#####



#status

@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Streaming(name=f"Prefix: - | Watching over {len(client.guilds)} Guilds ", url='https://www.twitch.tv/zzzloopy'))
    print(f"""
  
    ┏━━━┓╋╋┏┓╋┏┓
    ┃┏━┓┃╋╋┃┃┏┛┗┓
    ┃┗━━┳━━┫┃┣┓┏╋━━┓
    ┗━━┓┃┏┓┃┃┣┫┃┃━━┫
    ┃┗━┛┃┗┛┃┗┫┃┗╋━━┃
    ┗━━━┫┏━┻━┻┻━┻━━┛
    ╋╋╋╋┃┃
    ╋╋╋╋┗┛
  
    Logged into {client.user} 
    ID: {client.user.id}
    Guilds: {len(client.guilds)}
    Developed by Loopy#0001 >_<""")



#Prefix 
@client.command(aliases=['prefix'])
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f"The prefix in this server is now set to `{prefix}`")

#Antinuke

def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id

@client.listen("on_guild_join")
async def update_json(guild):
    with open('whitelist.json', 'r') as f:
        whitelisted = json.load(f)

    if str(guild.id) not in whitelisted:
        whitelisted[str(guild.id)] = []

    with open('whitelist.json', 'w') as f:
        json.dump(whitelisted, f, indent=4)

@client.command(aliases=['wld'], hidden=True)
async def whitelisted(ctx):

    embed = discord.Embed(title=f"Whitelisted users for {ctx.guild.name}",
                          description="")

    with open('whitelist.json', 'r') as i:
        whitelisted = json.load(i)
    try:
        for u in whitelisted[str(ctx.guild.id)]:
            embed.description += f"<@{(u)}> - {u}\n"
        await ctx.send(embed=embed)
    except KeyError:
        em = discord.Embed(description = f"nothing found in this guild")
        await ctx.send(embed=em) 

@whitelisted.error
async def whitelisted_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        em = discord.Embed(description = "Sorry but you don't have `administrator` permissions")
        await ctx.send(embed=em)

@client.command(aliases=['wl'])
@commands.check(is_server_owner)
async def whitelist(ctx,user: discord.Member = None):
    if user is None:
        em = discord.Embed(description = "You must specify a user to whitelist")
        await ctx.send(embed=em)
        return
    with open('whitelist.json', 'r') as f:
        whitelisted = json.load(f)

    if str(ctx.guild.id) not in whitelisted:
        whitelisted[str(ctx.guild.id)] = []
    else:
        if str(user.id) not in whitelisted[str(ctx.guild.id)]:
            whitelisted[str(ctx.guild.id)].append(str(user.id))
        else:
            em = discord.Embed(description = "That user is already whitelisted")
            await ctx.send(embed=em)
            return

    with open('whitelist.json', 'w') as f:
        json.dump(whitelisted, f, indent=4)
    em = discord.Embed(description = f"{user.mention} has been added to the whitelist")
    await ctx.send(embed = em)


@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        em = discord.Embed(description = "Only the guild owner can whitelist")
        await ctx.send(embed=em)


@client.command(aliases=['uwl'])
@commands.check(is_server_owner)
async def unwhitelist(ctx, user: discord.User = None):
    if user is None:
        em = discord.Embed(description = "You must specify a user to unwhitelist")
        await ctx.send(embed=em)
        return
    with open('whitelist.json', 'r') as f:
        whitelisted = json.load(f)
    try:
        if str(user.id) in whitelisted[str(ctx.guild.id)]:
            whitelisted[str(ctx.guild.id)].remove(str(user.id))

            with open('whitelist.json', 'w') as f:
                json.dump(whitelisted, f, indent=4)

            em = discord.Embed(description = f"{user.mention} has been removed from the whitelist", color = color)
            await ctx.send(embed=em)
    except KeyError:
        em = discord.Embed(description = "This user was never whitelisted", color = color)
        await ctx.send(embed=em)

@unwhitelist.error
async def unwhitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        em = discord.Embed(description = f"Only the guild owner can whitelist")
        await ctx.send(embed = em)

client.run("TOKEN_HERE_SKID")