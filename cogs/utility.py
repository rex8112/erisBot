import discord
import datetime
from discord.ext import commands


class Utility:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        """Makes the bot Pong"""
        embed = discord.Embed(colour=discord.Colour(0x9013fe), description='Pong!')
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.guild_only()
    async def whois(self, ctx, member: discord.Member):
        """Says when a user joined"""
        id = member.id
        av = member.avatar_url
        nick = member.nick
        status = member.status
        if member.activity:
            activity = member.activity.name
        joined = '{0.month}/{0.day}/{0.year} - {0.hour}:{0.minute}'.format(member.joined_at)
        created = '{0.month}/{0.day}/{0.year} - {0.hour}:{0.minute}'.format(member.created_at)
        
        
        embed = discord.Embed(colour=discord.Colour(0x9013fe))
        embed.set_author(name=member, icon_url=member.avatar_url)
        embed.set_image(url=av)
        embed.add_field(name="Identification",value=id,inline=True)
        embed.add_field(name="Nickname",value=nick,inline=True)
        embed.add_field(name="Status",value=status,inline=True)
        try:
            embed.add_field(name="Activity",value=activity,inline=True)
        except UnboundLocalError:
            pass
        embed.add_field(name="Joined At",value=joined,inline=True)
        embed.add_field(name='Created At',value=created,inline=True)
        embed.add_field(name='Image',value=av,inline=True)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.guild_only()
    async def users(self, ctx):
        """Lists User Count"""
        usrs = ctx.guild.member_count
        embed = discord.Embed(colour=discord.Colour(0x9013fe), description='**{0}** mortals exist in this Dimension'.format(usrs))
        embed.set_author(name=ctx.guild, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['sinfo'])
    @commands.guild_only()
    async def server(self, ctx):
        """Gives Current Server Information"""
        guild = ctx.guild
        embed = discord.Embed(colour=discord.Colour(0x9013fe))
        embed.set_author(name=guild, icon_url=guild.icon_url)
        embed.add_field(name='ID', value=guild.id)
        embed.add_field(name='Owner', value=guild.owner.mention)
        embed.add_field(name='Created', value='{0.month}/{0.day}/{0.year} - {0.hour}:{0.minute}'.format(guild.created_at))
        embed.add_field(name='Members', value=guild.member_count)
        embed.add_field(name='Channel Count', value=len(guild.channels) - len(guild.categories))
        embed.add_field(name='Region', value=guild.region)
        embed.add_field(name='Features', value=guild.features)
        embed.add_field(name='Image', value=guild.icon_url, inline=False)
        embed.set_image(url=guild.icon_url)
        
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.guild_only()
    async def jump(self, ctx, message):
        """Gets a Jump Url of supplied message
        Must be used in the same channel the message resides."""
        try:
            m = await ctx.get_message(message)
            embed = discord.Embed(colour=discord.Colour(0x9013fe), description='{}'.format(m.jump_url))
        except discord.NotFound:
            embed = discord.Embed(colour=discord.Colour(0x9013fe), description='Message Not Found: Make sure you run the command in the same channel as the message!')
        await ctx.author.send(embed=embed)
        await ctx.message.delete()
        
        
def setup(bot):
    bot.add_cog(Utility(bot))