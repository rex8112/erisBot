import discord
from discord.ext import commands

startup_extensions = ['cogs.admin',
					  'cogs.utility']

bot = commands.Bot(description='Testing some stuff', command_prefix='t.')

@bot.event
async def on_ready():
	print("Logged in as")
	print(bot.user.name)
	print(bot.user.id)
	print("----------")
	
	
	
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
	
	
	
bot.run("NDI4NDUwODI0NzY3OTMwMzY4.DZzgFA.8K1FENBzXj1lCMQ73ohEYwwNcyI")