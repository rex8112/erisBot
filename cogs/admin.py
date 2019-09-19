import datetime
import pytz
import discord
import logging
import sys
import cogs.tools.database as db


from discord.ext import commands
from cogs.tools.checks import *
from cogs.tools.configLoader import settings

logger = logging.getLogger('admin')

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *Reason):
        """Bans a user from the server"""
        if hierarchy(ctx, user):
            embed = discord.Embed(title="Banned", colour=discord.Colour(0x9013fe), description='You have been banned from **' + ctx.guild.name + '**', timestamp=datetime.datetime.now(tz=pytz.timezone('US/Central')))
            if Reason:
                Reason = ' '.join(Reason)
                embed.add_field(name='Reason', value=Reason)
            else:
                Reason = ''
            await user.send(embed=embed)
            await user.ban(reason=ctx.message.author.name + ' | ' + Reason)
            await ctx.message.add_reaction('✅')
            logger.warning('{} Banned {}'.format(ctx.author, user))
        else:
            raise commands.UserInputError('{} has more or equal power to you.'.format(user.mention))

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *Reason):
        """Kicks a user from the server"""
        if hierarchy(ctx, user):
            embed = discord.Embed(title="Kicked", colour=discord.Colour(0x9013fe), description='You have been kicked from **' + ctx.guild.name + '**', timestamp=datetime.datetime.now(tz=pytz.timezone('US/Central')))
            if Reason:
                Reason = ' '.join(Reason)
                embed.add_field(name='Reason', value=Reason)
            else:
                Reason = ''
            await user.send(embed=embed)
            await user.kick(reason=ctx.message.author.name + ' | ' + Reason)
            await ctx.message.add_reaction('✅')
            logger.warning('{} Kicked {}'.format(ctx.author, user))
        else:
            raise commands.UserInputError('{} has more or equal power to you.'.format(user.mention))
            
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, user: discord.Member, *, Reason):
        """Issues and Records a warning to a user"""
        if hierarchy(ctx, user):
            embed = discord.Embed(title="Warning", colour=discord.Colour(0x9013fe), timestamp=datetime.datetime.now(tz=pytz.timezone('US/Central')))
            embed.set_author(name=ctx.guild, icon_url=ctx.guild.icon_url)
            embed.add_field(name='Reason', value=Reason)
            
            await user.send(embed=embed)
            db.addWarn(user, Reason, ctx.author)
            await ctx.message.add_reaction('✅')
            logger.warning('{} Warned {}'.format(ctx.author, user))
        else:
            raise commands.UserInputError('{} has more or equal power to you.'.format(user.mention))
            
    @commands.command()
    @commands.is_owner()
    async def remWarn(self, ctx, indx):
        db.remWarn(indx)
        await ctx.message.add_reaction('✅')
        
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def pardon(self, ctx, indx):
        db.pardonWarn(indx)
        await ctx.message.add_reaction('✅')
            
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def warnings(self, ctx, user: discord.Member, *page):
        """Lists the current warnings a user has"""
        warns = db.getWarn(user)
        
        embed = discord.Embed(title="Warnings", colour=discord.Colour(0x9013fe))
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        for warn in warns:
            indx = warn[0]
            date = warn[5]
            reason = warn[3]
            state = warn[6]
            warner = self.bot.get_user(warn[4])
            if not warner:
                warner = "Unknown"
            
            if state:
                name = "~~{}: {} - {}~~".format(indx, str(warner), date)
                reason = '~~{}~~'.format(reason)
            else:
                name = "{}: {} - {}".format(indx, str(warner), date)
            embed.add_field(name=name, value=reason, inline=False)
        
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def awarnings(self, ctx, *page: int):
        """Lists 10 warnings from everyone"""
        
        embed = discord.Embed(title='Warnings', colour=discord.Colour(0x9013fe))
        if page:
            warns = db.getAllWarn(page[0])
            embed.set_footer(text='Page {}'.format(page[0]))
        else:
            warns = db.getAllWarn(1)
            embed.set_footer(text='Page {}'.format(1))
        
        for warn in warns:
            indx = warn[0]
            id = warn[2]
            date = warn[5]
            reason = warn[3]
            state = warn[6]
            usr = self.bot.get_user(id)
            warner = self.bot.get_user(warn[4])
            if not warner:
                warner = "Unknown"
            
            if state:
                name = "~~{}: {}: {}~~".format(indx, str(usr), date)
                reason = '~~{}~~'.format(reason)
            else:
                name = "{}: {}: {}".format(indx, str(usr), date)
            embed.add_field(name=name, value=reason, inline=False)
            
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, *, content):
        """Makes the bot say something"""
        await ctx.send(content)
        await ctx.message.delete()
    
    @commands.command()
    @commands.is_owner()
    async def send(self, ctx, channel: discord.TextChannel, *, content):
        """Makes the bot say something somewhere else"""
        try:
            await channel.send(content)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.send(content='Sorry {0},\n{1} is not a valid channel.'.format(ctx.message.author.name, channel), delete_after=5.00)
            
    @commands.command()
    @commands.is_owner()
    async def sendp(self, ctx, user: discord.Member, *, content):
        """Makes the bot say something to someone"""
        try:
            await user.send(content)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.send(content='Sorry {0},\n{1} is not a valid Member.'.format(ctx.message.author.name, user, delete_after=5.00))

    @commands.command()
    @commands.is_owner()
    async def setname(self, ctx, new: str):
        """Changes the username of the bot"""
        await self.bot.user.edit(username=new)
        logger.info('Bot name set to: {}'.format(new))
        
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Turns the bot off"""
        await ctx.send('Goodbye...')
        await self.bot.logout()
        sys.exit()
        
        
def setup(bot):
    bot.add_cog(Admin(bot))
