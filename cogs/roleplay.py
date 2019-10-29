import discord

from discord.ext import commands
import cogs.tools.database as db

class Roleplay(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.group(aliases=['rp'])
  @commands.guild_only()
  @commands.is_owner()
  async def roleplay(self, ctx):
    if ctx.invoked_subcommand is None:
      print('ree')
  
  @roleplay.command()
  async def new(self, ctx, name: str, private: bool, *members: discord.Member):
    guild = ctx.guild
    
    for role in guild.roles:
      if role.name == name:
        raise commands.UserInputError('Roleplay must have a unique name')
    
    role = await guild.create_role(name=name, mentionable=True, reason = 'RP {} | Init Role'.format(name))
    
    for mem in members:
      await mem.add_roles(role, reason = 'RP {} | Add Role'.format(name))
    
    if private:
      overwrites = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False),
        role: discord.PermissionOverwrite(send_messages=True, read_messages=True)
      }
    else:
      overwrites = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
        role: discord.PermissionOverwrite(send_messages=True)
      }
    
    category = await guild.create_category(name, overwrites=overwrites, reason='RP {} | Init Category'.format(name))
    await category.create_text_channel('ooc', topic='Out Of Character chat for {} Roleplay'.format(name))
    await category.create_text_channel('information', topic='Information Channel for {} Roleplay'.format(name))
    await category.create_text_channel('roleplay', topic='Roleplay Channel for {} Roleplay'.format(name))
    
    db.addRP(name, category.id, role.id, private)
      
  @roleplay.command()
  async def remove(self, ctx, rp: discord.CategoryChannel):
    guild = ctx.guild
    channels = rp.channels
    
    for ch in channels:
      await ch.delete(reason='{0.name} Deletion'.format(rp))
      
    await rp.delete(reason='{0.name} Deletion'.format(rp))
    
    for role in guild.roles:
      if role.name == rp.name:
        await role.delete(reason='{0.name} Deletion'.format(rp))
        
    db.delRP(rp.name)
  
def setup(bot):
  bot.add_cog(Roleplay(bot))