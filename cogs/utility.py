import discord
from discord.ext import commands


class UtilityCog:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	@commands.guild_only()
	async def ping(self, ctx):
		"""Makes the bot Pong"""
		await ctx.send('Pong!')
	
	@commands.command()
	@commands.guild_only()
	async def joined(self, ctx, member: discord.Member):
		"""Says when a user joined"""
		await ctx.send('{0.name} joined in {0.joined_at}'.format(member))
	
	@commands.command()
	@commands.guild_only()
	async def users(self, ctx):
		"""Lists User Count"""
		usrs = ctx.guild.member_count
		await ctx.send('{0} mortals exist in this Dimension'.format(usrs))
		
		
def setup(bot):
	bot.add_cog(UtilityCog(bot))