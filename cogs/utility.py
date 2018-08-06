import discord
import datetime
from discord.ext import commands


class Utility:
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
	async def whois(self, ctx, member: discord.Member):
		"""Says when a user joined"""
		id = member.id
		av = member.avatar_url
		nick = member.nick
		status = member.status
		activity = member.activity
		joined = '{0.month}/{0.day}/{0.year} - {0.hour}:{0.minute}'.format(member.joined_at)
		created = '{0.month}/{0.day}/{0.year} - {0.hour}:{0.minute}'.format(member.created_at)
		
		
		embed = discord.Embed(colour=discord.Colour(0x9013fe))
		embed.set_author(name=member, icon_url=member.avatar_url)
		embed.set_image(url=av)
		embed.add_field(name="Identification",value=id,inline=True)
		embed.add_field(name="Nickname",value=nick,inline=True)
		embed.add_field(name="Status",value=status,inline=True)
		embed.add_field(name="Activity",value=activity,inline=True)
		embed.add_field(name="Joined At",value=joined,inline=True)
		embed.add_field(name='Created At',value=created,inline=True)
		embed.add_field(name='Image',value=av,inline=True)
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
	bot.add_cog(Utility(bot))