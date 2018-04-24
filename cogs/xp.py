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
			user = ctx.author
			xp = getXP(user)
			lvl = getLVL(user)
			embed = discord.Embed(colour=discord.Colour(0x9013fe), description='**{}** is level **{}** and has **{}** XP'.format(user.mention, lvl, xp))
			await ctx.send(embed=embed)
	
	@xp.command()
	async def get(self, ctx, user: discord.Member):
		xp = getXP(user)
		lvl = getLVL(user)
		embed = discord.Embed(colour=discord.Colour(0x9013fe), description='**{}** is level **{}** and has **{}** XP'.format(user.mention, lvl, xp))
		await ctx.send(embed=embed)
	
	@xp.command()
	@commands.is_owner()
	async def set(self, ctx, user: discord.Member, amt: int):
		getXP(user)
		updateXP(user, amt)
		await ctx.message.add_reaction('✅')
	
	@xp.command()
	@commands.is_owner()
	async def add(self, ctx, user: discord.Member, amt: int):
		addXP(user, amt)
		await ctx.message.add_reaction('✅')
		
	@xp.command()
	@commands.is_owner()
	async def rem(self, ctx, user: discord.Member, amt: int):
		remXP(user, amt)
		await ctx.message.add_reaction('✅')
	
	
def setup(bot):
	bot.add_cog(XP(bot))