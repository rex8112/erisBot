import discord
from discord.ext import commands
from cogs.tools.matt import matt as m

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
    
    @commands.command()
    @commands.guild_only()
    async def matt(self, ctx):
        """Matt Dobbs Quotes"""
        quote = m.random()
        embed = discord.Embed(title='Quote Number: {}'.format(quote[0]), colour=discord.Colour(0x9013fe), description=quote[1])
        matthew = ctx.guild.get_member(106893131978395648)
        embed.set_author(name=matthew.name, icon_url=matthew.avatar_url)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Meme(bot))