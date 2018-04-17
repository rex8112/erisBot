import discord
from discord.ext import commands
from cogs.tools.database import *


class XP:
	def __init__(self, bot):
		self.bot = bot
		initDB()
	
	@commands.group()
	@commands.guild_only()
	async def xp(self, ctx):
		if ctx.invoked_subcommand is None:
			raise commands.UserInputError('Missing Subcommands')
	
	@xp.command()
	async def get(self, ctx, mem: discord.Member):
		xp = getXP(mem)
		await ctx.send('{} has {} XP'.format(mem.name, xp))
	
	@xp.command()
	async def set(self, ctx, mem: discord.Member, amt: int):
		if getXP(mem):
			updateXP(mem, amt)
		elif getXP(mem) is None:
			addMem(mem)
			updateXP(mem, amt)
	
def setup(bot):
	bot.add_cog(XP(bot))