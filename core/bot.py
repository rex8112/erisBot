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
	await ctx.send('Goodbye...')
	await bot.logout()
	sys.exit()
		
@bot.command()
async def say(ctx, *, content):
	await ctx.send(content)
	await ctx.message.delete()
	
@bot.command()
async def send(ctx, channel, *, content):
	try:
		dest = list(channel)
		dest = int(''.join(dest[2:-1]))
		print(dest)
		dest = bot.get_channel(dest)
		await dest.send(content)
	except:
		await ctx.send(content='Sorry {0},\n{1} is not a valid channel.'.format(ctx.message.author.mention, channel), delete_after=5.00)

@bot.command()
async def setname(ctx, new: str):
	await bot.user.edit(username=new)

	
	
	
	
	
	
bot.run("TOKEN")