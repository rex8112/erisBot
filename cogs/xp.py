import discord
from discord.ext import commands


class XP:
	def __init__(self, bot):
		self.bot = bot
	
	
def setup(bot):
	bot.add_cog(XP(bot))