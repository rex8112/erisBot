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
			xp = getXP(ctx.author)
			embed = discord.Embed(colour=discord.Colour(0x9013fe), description='You have **{}** XP'.format(xp))
			await ctx.send(embed=embed)
	
	@xp.command()
	async def get(self, ctx, mem: discord.Member):
		xp = getXP(mem)
		embed = discord.Embed(colour=discord.Colour(0x9013fe), description='**{}** has **{}** XP'.format(mem.mention, xp))
		await ctx.send(embed=embed)
	
	@xp.command()
	@commands.is_owner()
	async def set(self, ctx, mem: discord.Member, amt: int):
		if getXP(mem):
			updateXP(mem, amt)
		elif getXP(mem) is None:
			addMem(mem)
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