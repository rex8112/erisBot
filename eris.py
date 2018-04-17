import datetime
import discord
from discord.ext import commands
from config.config import __token__, __logid__

startup_extensions = ['cogs.admin', 'cogs.utility', 'cogs.xp']

bot = commands.Bot(description='Testing some stuff', command_prefix='t.')

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
	
@bot.event
async def on_command_completion(ctx):
	log = bot.get_channel(__logid__)
	if log is None:
		return
		
	embed = discord.Embed(title="{}".format(ctx.command), colour=discord.Colour(0x9013fe), description="in {}\nby {}".format(ctx.message.channel, ctx.message.author.mention), timestamp=datetime.datetime.now())
	embed.set_author(name="Command Invoked")
	embed.add_field(name="Full Command:", value="{}".format(ctx.message.content))

	await log.send(embed=embed)
	
	
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
	
	
bot.run(__token__)