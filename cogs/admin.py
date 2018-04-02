import discord
from discord.ext import commands


class AdminCog:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	@commands.is_owner()
	async def say(self, ctx, *, content):
		await ctx.send(content)
		await ctx.message.delete()
	
	@commands.command()
	@commands.is_owner()
	async def send(self, ctx, channel, *, content):
		try:
			dest = list(channel)
			dest = int(''.join(dest[2:-1]))
			print(dest)
			dest = bot.get_channel(dest)
			await dest.send(content)
		except:
			await ctx.send(content='Sorry {0},\n{1} is not a valid channel.'.format(ctx.message.author.mention, channel), delete_after=5.00)

	@commands.command()
	@commands.is_owner()
	async def setname(self, ctx, new: str):
		await bot.user.edit(username=new)
		
	@commands.command()
	@commands.is_owner()
	async def shutdown(self, ctx):
		"""Turns the bot off"""
		await ctx.send('Goodbye...')
		await bot.logout()
		sys.exit()
		
		
def setup(bot):
	bot.add_cog(AdminCog(bot))