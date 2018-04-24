import datetime
import pytz
import discord


from discord.ext import commands
from cogs.tools.checks import *
from config.configLoader import settings


class AdminCog:
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user: discord.Member = None, *Reason):
		if hierarchy(ctx, user):
			embed = discord.Embed(title="Banned", colour=discord.Colour(0x9013fe), description='You have been banned from **' + ctx.guild.name + '**', timestamp=datetime.datetime.now(tz=pytz.timezone('US/Central')))
			if type(Reason) is not NoneType:
				Reason = ' '.join(Reason)
				embed.add_field(name='Reason', value=Reason)
			else:
				Reason = ''
			await user.send(embed=embed)
			await user.ban(reason=ctx.message.author.name + ' | ' + Reason)
		else:
			raise commands.UserInputError('{} has more or equal power to you.'.format(user.name))

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, user: discord.Member = None, *Reason):
		if hierarchy(ctx, user):
			embed = discord.Embed(title="Kicked", colour=discord.Colour(0x9013fe), description='You have been kicked from **' + ctx.guild.name + '**', timestamp=datetime.datetime.now(tz=pytz.timezone('US/Central')))
			if Reason:
				Reason = ' '.join(Reason)
				embed.add_field(name='Reason', value=Reason)
			else:
				Reason = ''
			await user.send(embed=embed)
			await user.kick(reason=ctx.message.author.name + ' | ' + Reason)
		else:
			raise commands.UserInputError('{} has more or equal power to you.'.format(user.name))

	@commands.command()
	@commands.is_owner()
	async def say(self, ctx, *, content):
		await ctx.send(content)
		await ctx.message.delete()
	
	@commands.command()
	@commands.is_owner()
	async def send(self, ctx, channel: discord.TextChannel, *, content):
		try:
			await channel.send(content)
		except:
			await ctx.send(content='Sorry {0},\n{1} is not a valid channel.'.format(ctx.message.author.name, channel), delete_after=5.00)
			
	@commands.command()
	@commands.is_owner()
	async def sendp(self, ctx, user: discord.Member, *, content):
		try:
			await user.send(content)
		except:
			await ctx.send(content='Sorry {0},\n{1} is not a valid Member.'.format(ctx.message.author.name, player, delete_after=5.00))

	@commands.command()
	@commands.is_owner()
	async def setname(self, ctx, new: str):
		await bot.user.edit(username=new)
		
	@commands.command()
	@commands.is_owner()
	async def shutdown(self, ctx):
		"""Turns the bot off"""
		await ctx.send('Goodbye...')
		await self.bot.logout()
		sys.exit()
		
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.NoPrivateMessage):
			print(error)
			await ctx.send('[NoPrivateMessage] Sorry. This command is not allow in private messages.')
		else:
			print(error)
			await ctx.send(content=error, delete_after=5.00)
		
def setup(bot):
	bot.add_cog(AdminCog(bot))
