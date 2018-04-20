import discord
import random
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
			mem = ctx.author
			xp = getXP(mem)
			lvl = getLVL(mem)
			embed = discord.Embed(colour=discord.Colour(0x9013fe), description='**{}** is level **{}** and has **{}** XP'.format(mem.mention, lvl, xp))
			await ctx.send(embed=embed)
	
	@xp.command()
	async def get(self, ctx, mem: discord.Member):
		xp = getXP(mem)
		lvl = getLVL(mem)
		embed = discord.Embed(colour=discord.Colour(0x9013fe), description='**{}** is level **{}** and has **{}** XP'.format(mem.mention, lvl, xp))
		await ctx.send(embed=embed)
	
	@xp.command()
	@commands.is_owner()
	async def set(self, ctx, mem: discord.Member, amt: int):
		getXP(mem)
		updateXP(mem, amt)
	
	async def on_message(self, ctx):
		mem = ctx.author
		amt = random.randint(10, 15)
		if not mem.bot:
			if getXP(mem):
				addXP(mem, amt)
			else:
				addMem(mem)
				addXP(mem, amt)
	
def setup(bot):
	bot.add_cog(XP(bot))