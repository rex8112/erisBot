import discord
import random
import datetime
import pytz
import logging


from discord.ext import commands
from cogs.tools.database import database as db
from cogs.xp import XP as XP
from config.configLoader import settings

logger = logging.getLogger('events')

class events:
	def __init__(self, bot):
		self.bot = bot
	async def on_message(self, ctx):
		user = ctx.author
		if not user.bot:
		
			#Adds XP per message in a Guild
			if ctx.guild:
				logger.debug('Begin XP Gain: {}'.format(user))
				lvl = db.getLVL(user)
				oxp = db.getXP(user)
				logger.debug('Level: {} XP: {}'.format(lvl, oxp))
				amt = random.randint(10, 15)
				logger.debug('Amount: {}'.format(amt))
				db.addXP(user, amt)
				nxp = db.getXP(user)
				logger.debug('New XP: {}'.format(nxp))
				logger.info('{}: Old XP: {} New XP: {}'.format(user, oxp, nxp))
				goal = 300 + (lvl * 100)
				if oxp < goal and nxp >= goal:
					embed = discord.Embed(title="Can Level Up", colour=discord.Colour(0xbd10e0), description="Congratulations **{}**! You have reached enough **{}** to **level up**".format(user.mention, XP.xpName))
					embed.set_thumbnail(url=user.avatar_url)
					
					await ctx.channel.send(embed=embed, delete_after=10.00)
					
			#Messages Owner when receiving a DM
			if not ctx.guild:
				owner = self.bot.get_user(int(settings.owner))
				if ctx.author is not owner:
					embed = discord.Embed(description=ctx.content, colour=discord.Colour(0x9013fe), timestamp=datetime.datetime.now(tz=pytz.timezone('US/Central')))
					embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
					await owner.send(embed=embed)

	async def on_command_completion(self, ctx):
		try:
			log = self.bot.get_channel(int(settings.logid))
			if log is None:
				return
				
			embed = discord.Embed(title="{}".format(ctx.command), colour=discord.Colour(0x9013fe), description="in {}\nby {}".format(ctx.message.channel, ctx.message.author.mention), timestamp=datetime.datetime.now(tz=pytz.timezone('US/Central')))
			embed.set_author(name="Command Invoked")
			embed.add_field(name="Full Command:", value="{}".format(ctx.message.content))

			await log.send(embed=embed)
		except ValueError:
			return
		
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.NoPrivateMessage):
			print(error)
			await ctx.send('[NoPrivateMessage] Sorry. This command is not allow in private messages.')
		else:
			print(error)
			embed = discord.Embed(title="Error", colour=discord.Colour(0xd0021b), description=str(error))
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed, delete_after=5.00)
		
def setup(bot):
	bot.add_cog(events(bot))