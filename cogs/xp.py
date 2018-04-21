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
		await ctx.message.add_reaction('✅')
	
	@xp.command()
	@commands.is_owner()
	async def add(self, ctx, mem: discord.Member, amt: int):
		addXP(mem, amt)
		
	@xp.command()
	@commands.is_owner()
	async def rem(self, ctx, mem: discord.Member, amt: int):
		remXP(mem, amt)
	
	async def on_message(self, ctx): #XP Gain Via Messages
		mem = ctx.author
		if not mem.bot:
			olvl = getLVL(mem)
			amt = random.randint(10, 15)
			addXP(mem, amt)
			nlvl = getLVL(mem)
			if olvl < nlvl:
				print('{} leveled up'.format(mem))
				embed = discord.Embed(title="Leveled Up", colour=discord.Colour(0xbd10e0), description="Congratulations **{}**! You have reached **level {}**".format(mem.mention, nlvl))
				embed.set_thumbnail(url=mem.avatar_url)
				
				await ctx.channel.send(embed=embed, delete_after=10.00)
	
def setup(bot):
	bot.add_cog(XP(bot))