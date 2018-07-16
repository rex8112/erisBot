import datetime
import pytz
import discord


from discord.ext import commands
from config.configLoader import settings

startup_extensions = ['cogs.admin', 'cogs.utility', 'cogs.xp', 'cogs.events', 'cogs.meme']

bot = commands.Bot(description='Created by rex8112', command_prefix='t.', owner_id=int(settings.owner))

@bot.event
async def on_ready():
	print("Logged in as")
	print('Name: {}'.format(bot.user.name))
	print('ID:   {}'.format(bot.user.id))
	print("----------")
	for guild in bot.guilds:
		print(guild.name)
		print(guild.id)
		print('----------')
	game = discord.Activity(name='mortals', type=discord.ActivityType.listening)
	await bot.change_presence(status=discord.Status.idle, activity=game)
	
	
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
	
	
bot.run(settings.token)
