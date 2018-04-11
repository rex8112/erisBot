import discord
from discord.ext import commands


class AdminCog:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, mem: discord.Member = None, *Reason):
		if mem is not None:
			if Reason:
				Reason = ' '.join(Reason)
			else:
				Reason = None
			await mem.kick(reason=Reason)
		else:
			await ctx.send(content='Incorrect Member', delete_after=5.00)

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
	async def sendp(self, ctx, player: discord.Member, *, content):
		try:
			await player.send(content)
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
