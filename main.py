import discord
from discord.ext import commands
import os
import requests
import json
import keep_alive
keep_alive.keep_alive()

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes.get(str(message.guild.id), "-")

loopylol = commands.Bot(command_prefix=get_prefix,
                      case_insensitive=True,
                      intents=intents)
loopylol.remove_command("help")

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    loopylol.load_extension(f'cogs.{filename[:-3]}')

#status

@loopylol.event
async def on_ready():
    await loopylol.change_presence(
        activity=discord.Streaming(name=f"Prefix: - | Watching over {len(loopylol.guilds)} Guilds ", url='https://www.twitch.tv/zzzloopy'))
    print(f"""
    Logged into {loopylol.user} 
    ID: {loopylol.user.id}
    Guilds: {len(loopylol.guilds)}
    Developed by Loopy#0001 >_<""")

#Prefix 

@loopylol.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '-'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@loopylol.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@loopylol.command(aliases=['prefix'])
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

@loopylol.listen("on_guild_join")
async def update_json(guild):
    with open('whitelist.json', 'r') as f:
        whitelisted = json.load(f)

    if str(guild.id) not in whitelisted:
        whitelisted[str(guild.id)] = []

    with open('whitelist.json', 'w') as f:
        json.dump(whitelisted, f, indent=4)

@loopylol.command(aliases=['wld'], hidden=True)
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

@loopylol.command(aliases=['wl'])
@commands.check(is_server_owner)
async def whitelist(ctx,user: discord.User = None):
    if user is None:
        await ctx.send("You must specify a user to whitelist")
        return
    with open('whitelist.json', 'r') as f:
        whitelisted = json.load(f)

    if str(ctx.guild.id) not in whitelisted:
        whitelisted[str(ctx.guild.id)] = []
    else:
        if str(user.id) not in whitelisted[str(ctx.guild.id)]:
            whitelisted[str(ctx.guild.id)].append(str(user.id))
        else:
            await ctx.send("That user is already whitelisted")
            return

    with open('whitelist.json', 'w') as f:
        json.dump(whitelisted, f, indent=4)
    await ctx.send(f"{user.mention} has been added to the whitelist")

@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Only the guild owner can whitelist")

@loopylol.command(aliases=['uwl'])
@commands.check(is_server_owner)
async def unwhitelist(ctx, user: discord.User = None):
    if user is None:
        await ctx.send("You must specify a user to unwhitelist")
        return
    with open('whitelist.json', 'r') as f:
        whitelisted = json.load(f)
    try:
        if str(user.id) in whitelisted[str(ctx.guild.id)]:
            whitelisted[str(ctx.guild.id)].remove(str(user.id))
            with open('whitelist.json', 'w') as f:
                json.dump(whitelisted, f, indent=4)
            await ctx.send(f"{user.mention} has been removed from the whitelist")
    except KeyError:
              await ctx.send("This user was never whitelisted")

@unwhitelist.error
async def unwhitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Only the guild owner can unwhitelist")

loopylol.run("TOKEN_HERE_SKID")