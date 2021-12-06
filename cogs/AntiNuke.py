import discord
import json
from discord.ext import commands
import datetime

class AntiNuke(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
      with open('whitelist.json') as f:
        whitelisted = json.load(f)
      async for i in channel.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_create):
          if str(i.user.id) in whitelisted[str(channel.guild.id)]:
            return
          

          await channel.guild.kick(i.user,reason="AntiNuke: Creating Channels")
          await i.target.delete(reason=f"AntiNuke: Deleting user created channels")
          await i.target.delete(reason=f"AntiNuke: Deleting user created channels")
          await i.target.delete(reason=f"AntiNuke: Deleting user created channels")
          await i.target.delete(reason=f"AntiNuke: Deleting user created channels")
          await i.target.delete(reason=f"AntiNuke: Deleting user created channels")
          await i.target.delete(reason=f"AntiNuke: Deleting user created channels")
          return
        
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
      with open('whitelist.json') as f:
        whitelisted = json.load(f)
      async for i in channel.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_delete):
          if str(i.user.id) in whitelisted[str(channel.guild.id)]:
            return
          await channel.guild.kick(i.user,reason="Splits AntiNuke: Deleting Channels")
          return


    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
      with open('whitelist.json') as f:
        whitelisted = json.load(f)
      async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.ban):
      
          if str(i.user.id) in whitelisted[str(guild.id)]:
            return
    
          await guild.ban(i.user, reason="AntiNuke: Banning Members")
          await guild.ban(i.user, reason="AntiNuke: Banning Members")
          return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
      with open('whitelist.json') as f:
        whitelisted = json.load(f)
      async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.kick):
      
          if str(i.user.id) in whitelisted[str(i.guild.id)]:
            return
          if i.target.id == member.id:
             await i.user.kick()
             return

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
      with open('whitelist.json') as f:
        whitelisted = json.load(f)
      async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_create):
        if i.user.bot:
            return
      
        if str(i.user.id) in whitelisted[str(role.guild.id)]:
            return
    
        await role.guild.kick(i.user, reason="Creating Roles")
        await i.target.delete()
        return
        
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
      with open('whitelist.json') as f:
        whitelisted = json.load(f)
      async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_delete):
          if i.user.bot:
              return
      
          if str(i.user.id) in whitelisted[str(role.guild.id)]:
              return
    
          await role.guild.kick(i.user, reason="Antinuke: Deleting Roles")
          await i.target.clone()
          return

    @commands.Cog.listener()
    async def on_webhook_update(self, webhook):
      with open('whitelist.json') as f:
        whitelisted = json.load(f)
      async for i in webhook.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.webhook_create):
          if str(i.user.id) in whitelisted[str(webhook.guild.id)]:
            return
          

          await webhook.guild.kick(reason="AntiNuke: Creating Webhooks")
          await i.target.delete()
          return

def setup(client):
    client.add_cog(AntiNuke(client))