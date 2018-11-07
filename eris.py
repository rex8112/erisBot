import datetime
import pytz
import discord
import asyncio
import logging


from discord.ext import commands
from cogs.tools.configLoader import settings
from cogs.tools.database import database as db

startup_extensions = ['cogs.admin', 'cogs.utility', 'cogs.xp', 'cogs.events', 'cogs.meme']

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
    bg_task = bot.loop.create_task(degrade())
    logger.info('----- Bot Startup Complete -----')

async def degrade():
    while True:
        now = datetime.datetime.now()
        then = (now + datetime.timedelta(days=1)).replace(hour = 0, minute = 0, second = 0)
        delta = then - now
        secs = delta.seconds
        logger.info('Waiting {} seconds for degrade'.format(secs))
        await asyncio.sleep(secs)
        
        users = db.getAllUsers()
        for user in users: #Iterates through all users
            lvl = user[4]
            xp = user[3]
            id = user[2]
            usr = bot.get_user(id)
            amt = 10 + (lvl * 1)
            
            try:
                if lvl <= 0 and xp - amt < 0: #If running out of XP with no levels to sell
                    db.updateXP(usr, 0)
                elif xp - amt < 0: #If running out of XP with levels to sell
                    lvl = lvl - 1
                    sell = 300 + (lvl * 100)
                    remain = amt - xp
                    xp = sell - remain
                    db.updateLVL(usr, lvl)
                    db.updateXP(usr, xp)
                    
                    embed = discord.Embed(title = 'Level Lost', colour = discord.Colour(0xd0021b), description = 'Due to low-activity you have lost a level and are now Level **{}**'.format(lvl))
                    await user.send(embed=embed)
                    logger.info('Removing Level: {}'.format(usr))
                else: #Only remaining option is there is XP left to take
                    db.remXP(usr, amt)
                    logger.debug('Removing {} XP from {}'.format(amt, usr))
            except AttributeError:
                db.remMem(id)
        
    
    
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    
    
bot.run(settings.token)
