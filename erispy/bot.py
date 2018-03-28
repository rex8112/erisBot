import discord
from discord.ext import commands

bot = commands.Bot(description='Testing some stuff', command_prefix='t.')

@bot.event
async def on_ready():
	print("Logged in as")
	print(bot.user.name)
	print(bot.user.id)
	print("----------")
	
@bot.command()
async def ping(ctx):
	"""Makes the bot Pong"""
	await ctx.send('Pong!')
	
@bot.command()
async def joined(ctx, member : discord.Member):
	"""Says when a user joined"""
	await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

	
	
	
	
	
	
bot.run("TOKEN")