import discord
from discord.ext import commands
from cogs.tools.database import *


class XP:
	def __init__(self, bot):
		self.bot = bot
		initDB()
	
	@commands.command()
	@commands.guild_only()
	async def setXP(self, ctx, mem: discord.Member, amt: int):
		if getXP(mem):
			updateXP(mem, amt)
		elif getXP(mem) is None:
			addMem(mem)
			updateXP(mem, amt)
	
	@commands.command()
	@commands.guild_only()
	async def retrieveXP(self, ctx, mem: discord.Member):
		xp = getXP(mem)
		await ctx.send('{} has {} XP'.format(mem.name, xp))
	
def setup(bot):
	bot.add_cog(XP(bot))