import discord
from discord.ext import commands


class UtilityCog:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	@commands.guild_only()
	async def ping(self, ctx):
		"""Makes the bot Pong"""
		embed = discord.Embed(colour=discord.Colour(0x9013fe), description='Pong!')
		await ctx.send(embed=embed)
	
	@commands.command()
	@commands.guild_only()
	async def joined(self, ctx, member: discord.Member):
		"""Says when a user joined"""
		embed = discord.Embed(colour=discord.Colour(0x9013fe), description='{0.mention} joined in {0.joined_at}'.format(member))
		embed.set_author(name=member.name, icon_url=member.avatar_url)
		await ctx.send(embed=embed)
	
	@commands.command()
	@commands.guild_only()
	async def users(self, ctx):
		"""Lists User Count"""
		usrs = ctx.guild.member_count
		embed = discord.Embed(colour=discord.Colour(0x9013fe), description='**{0}** mortals exist in this Dimension'.format(usrs))
		embed.set_author(name=ctx.guild, icon_url=ctx.guild.icon_url)
		await ctx.send(embed=embed)
		
		
def setup(bot):
	bot.add_cog(UtilityCog(bot))