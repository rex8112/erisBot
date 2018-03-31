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
	
@bot.command()
async def users(ctx):
	"""Lists Users Count"""
	usrs = len(bot.users)
	await ctx.send('{0} mortals exist in this Dimension'.format(usrs))
	
@bot.command()
async def shutdown(ctx):
	"""Turns the bot off"""
	if bot.is_owner(discord.Message.author):
		await ctx.send('Goodbye...')
		await bot.logout()
		sys.exit()

@bot.command()
async def name(ctx, new):
	await discord.ClientUser.edit(username=new)

	
	
	
	
	
	
bot.run("TOKEN")