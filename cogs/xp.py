import discord
from discord.ext import commands
from cogs.tools.database import database as db


class XP:
	def __init__(self, bot):
		self.bot = bot
		db.initDB()
	
	@commands.group()
	@commands.guild_only()
	async def xp(self, ctx):
		"""Retrieves your current XP and level"""
		if ctx.invoked_subcommand is None:
			user = ctx.author
			xp = db.getXP(user)
			lvl = db.getLVL(user)
			goal = 300 + (lvl * 100)
			remaining = goal - xp
			embed = discord.Embed(colour=discord.Colour(0x9013fe), description='**{}** is level **{}** and has **{}** XP'.format(user.mention, lvl, xp))
			if remaining <= 0:
				embed.add_field(name = 'Can Level Up', value = '**{}** XP Required'.format(goal))
			else:
				embed.add_field(name = 'Next Level Up', value = '**{}** XP Remaining'.format(remaining))
			await ctx.send(embed=embed)
	
	@xp.command()
	async def get(self, ctx, user: discord.Member):
		"""Get the XP of another User"""
		xp = db.getXP(user)
		lvl = db.getLVL(user)
		embed = discord.Embed(colour=discord.Colour(0x9013fe), description='**{}** is level **{}** and has **{}** XP'.format(user.mention, lvl, xp))
		await ctx.send(embed=embed)
	
	@xp.command()
	@commands.is_owner()
	async def set(self, ctx, user: discord.Member, amt: int):
		"""Set the XP of a User"""
		db.getXP(user)
		db.updateXP(user, amt)
		await ctx.message.add_reaction('✅')
	
	@xp.command()
	@commands.is_owner()
	async def add(self, ctx, user: discord.Member, amt: int):
		"""Add XP to a User"""
		db.addXP(user, amt)
		await ctx.message.add_reaction('✅')
		
	@xp.command()
	@commands.is_owner()
	async def rem(self, ctx, user: discord.Member, amt: int):
		"""Remove XP from a User"""
		db.remXP(user, amt)
		await ctx.message.add_reaction('✅')
	
	@commands.command()
	@commands.guild_only()
	async def levelup(self, ctx):
		user = ctx.author
		xp = db.getXP(user)
		lvl = db.getLVL(user)
		goal = 300 + (lvl * 100)
		if xp >= goal:
			lvl = db.addLVL(user, 1)
			xp = db.remXP(user, goal)
			embed = discord.Embed(title='Leveled Up', colour=discord.Colour(0x9013fe), description='You have spent **{}** XP and acquired level **{}**!'.format(goal, lvl))
			goal = 300 + (lvl * 100)
		else:
			embed = discord.Embed(title='Failed to Level Up', colour=discord.Colour(0xd0021b), description='You do not have enough XP')
		embed.add_field(name='Current XP', value='**{}**'.format(xp), inline=True)
		embed.add_field(name='Current Level', value='**{}**'.format(lvl), inline=True)
		embed.add_field(name='To Level Up', value='**{}** XP'.format(goal), inline=True)
		embed.set_author(name=user.name, icon_url=user.avatar_url)
		await ctx.send(embed=embed)
	
def setup(bot):
	bot.add_cog(XP(bot))