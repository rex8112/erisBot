import discord
from discord.ext import commands

def hierarchy(ctx, mem: discord.Member):
	invoker = ctx.author
	clen = len(invoker.roles) - 1
	mlen = len(mem.roles) - 1
	if invoker == ctx.guild.owner:
		return True
	if invoker.roles[clen] > mem.roles[mlen]:
		return True
	else:
		return False