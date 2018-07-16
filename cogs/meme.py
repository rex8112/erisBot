import discord
from discord.ext import commands

class Meme:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 10, type=commands.BucketType.user)
	async def thankyou(self, ctx):
		"""Thank you, very cool."""
		embed = discord.Embed(colour=discord.Colour(0x9013fe), description='Thank you {}, very cool.'.format(ctx.author.mention))
		await ctx.send(embed=embed)
		await ctx.message.delete()
		
def setup(bot):
	bot.add_cog(Meme(bot))