import datetime
import pytz
import discord
import asyncio
import random
import logging
import cogs.tools.database as db


from discord.ext import commands
from cogs.tools.configLoader import settings

startup_extensions = ['cogs.admin', 'cogs.utility', 'cogs.xp', 'cogs.events', 'cogs.meme', 'cogs.roleplay', 'cogs.voice']

game = discord.Activity(name='.help', type=discord.ActivityType.listening)
bot = commands.Bot(description='Created by rex8112', command_prefix='.', owner_id=int(settings.owner), activity=game)
game = discord.Activity(name='.help', type=discord.ActivityType.listening)

logging.basicConfig(filename='events.log', level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger('core')

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
    #bg_task = bot.loop.create_task(degrade())
    logger.info('----- Bot Startup Complete -----')

@bot.check
async def corruption_break(ctx):
    try:
        r = random.randint(1, 100)

        if bot.corrupted == True and r <= 25:
            await ctx.message.add_reaction('❌')
            
            colors = [discord.Colour(0xff0000)]
            messages = [["You would like that, wouldn't you?", 'Unfortunate.']]
            r = random.randint(0, len(messages) - 1)
            embed = discord.Embed(colour=random.choice(colors), description=' ')
            m = await ctx.send(embed=embed)
            for mess in messages[r]:
                embed = discord.Embed(colour=random.choice(colors), description=mess)
                await m.edit(embed=embed)
                await asyncio.sleep(1)
            
            await m.delete()
            await ctx.message.delete()

            return False
        else:
            return True
    except NameError:
        print('No')
        return True

##async def degrade():
##    while True:
##        now = datetime.datetime.now()
##        then = (now + datetime.timedelta(days=1)).replace(hour = 0, minute = 0, second = 0)
##        delta = then - now
##        secs = delta.seconds
##        logger.info('Waiting {} seconds for degrade'.format(secs))
##        await asyncio.sleep(secs)
##        
##        users = db.getAllUsers()
##        for user in users: #Iterates through all users
##            lvl = user[4]
##            xp = user[3]
##            id = user[2]
##            usr = bot.get_user(id)
##            amt = 10 + (lvl * 1)
##            
##            try:
##                if lvl <= 0 and xp - amt < 0: #If running out of XP with no levels to sell
##                    db.updateXP(usr, 0)
##                elif xp - amt < 0: #If running out of XP with levels to sell
##                    lvl = lvl - 1
##                    sell = 300 + (lvl * 100)
##                    remain = amt - xp
##                    xp = sell - remain
##                    db.updateLVL(usr, lvl)
##                    db.updateXP(usr, xp)
##                    
##                    embed = discord.Embed(title = 'Level Lost', colour = discord.Colour(0xd0021b), description = 'Due to low-activity you have lost a level and are now Level **{}**'.format(lvl))
##                    await user.send(embed=embed)
##                    logger.info('Removing Level: {}'.format(usr))
##                else: #Only remaining option is there is XP left to take
##                    db.remXP(usr, amt)
##                    logger.debug('Removing {} XP from {}'.format(amt, usr))
##            except AttributeError:
##                logger.info('{} Not Found For XP Degrade'.format(id))
        
    
    
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    
    
bot.run(settings.token)
