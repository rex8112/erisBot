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
	
	async def on_message(self, ctx): #XP Gain Via Messages
		user = ctx.author
		if not user.bot:
			olvl = getLVL(user)
			amt = random.randint(10, 15)
			addXP(user, amt)
			nlvl = getLVL(user)
			if olvl < nlvl:
				print('{} leveled up'.format(user))
				embed = discord.Embed(title="Leveled Up", colour=discord.Colour(0xbd10e0), description="Congratulations **{}**! You have reached **level {}**".format(user.mention, nlvl))
				embed.set_thumbnail(url=user.avatar_url)
				
				await ctx.channel.send(embed=embed, delete_after=10.00)
	
def setup(bot):
	bot.add_cog(XP(bot))