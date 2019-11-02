import discord
import datetime
import logging
import asyncio
import os
import cogs.tools.database as db
import random
import string

from discord.ext import tasks, commands
from discord.utils import get

logger = logging.getLogger('corruption')

class Data:
    guildID = 180069417625845760
    guild = None
    chan = None
    mess = []
    startTime = datetime.time(hour=23, minute = 0, second=0)
    endTime = datetime.time(hour=5, minute=0, second=0)

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.corrupted = None
        self.corruptionController.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('test')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def invade(self, ctx, ch: discord.VoiceChannel):
        """Connect to VC"""
        voice = get(self.bot.voice_clients, guild=Data.guild)

        if voice and voice.is_connected():
            await voice.move_to(ch)
        else:
           voice = await ch.connect()

        _ = os.path.isfile("sound.mp3")
        await asyncio.sleep(5)
        voice.play(discord.FFmpegPCMAudio("sound.mp3"), after=lambda e: print("Sound done!"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.1
        await asyncio.sleep(30)
        await voice.disconnect()
        
    # @commands.command()
    # @commands.guild_only()
    # async def play(self, ctx):
    #     _ = os.path.isfile("song.mp3")
    #     voice = get(self.bot.voice_clients, guild=ctx.guild)
    #     voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    #     voice.source = discord.PCMVolumeTransformer(voice.source)
    #     voice.source.volume = 0.07
    # @commands.command()
    # @commands.guild_only()
    # async def testMessage(self, ctx, ch: discord.TextChannel):
    #     s = 'HelpMe'
    #     m = ''.join(random.sample(s, len(s)))
    #     message = await ch.send(embed=self.getEmbed(' ', 500))
    #     for l in m:
    #         embed = self.getEmbed(l, 500)
    #         await message.edit(embed=embed)
    #         await asyncio.sleep(5)
    #     await message.delete()

    @tasks.loop(minutes=10)
    async def corruptionController(self):
        now = datetime.datetime.now()
        startTime = datetime.datetime.now().replace(hour=Data.startTime.hour, minute=Data.startTime.minute, second=Data.startTime.second)
        endTime = datetime.datetime.now().replace(hour=Data.endTime.hour, minute=Data.endTime.minute, second=Data.endTime.second)

        if self.bot.corrupted == None:
            if self.bot.user.name != 'Eris':
                self.bot.corrupted = True
            else:
                self.bot.corrupted = False
        
        if now >= startTime or endTime < now: #If it's inside of the corruption time
            if self.bot.corrupted == False:
                print('Immediately corrupting for catch up')
                await self.corrupt()
            elif not self.randomMessage.get_task(): #In the event the bot died and came back during corruption, it won't go through corrupt() and start randomMessage()
                self.randomMessage.start()
                print('Restarting Random Messages')
            
            delta = endTime - now
            if delta.days < 0:
                delta += datetime.timedelta(days=1)

            print('Waiting {} seconds for uncorruption'.format(delta.seconds))
            await asyncio.sleep(delta.seconds)
            await self.uncorrupt()

        else: #Only other option is outside of the corruption time
            if self.bot.corrupted == True:
                print('Immediately uncorrupting for catch up')
                await self.uncorrupt()

            delta = startTime - now
            if delta.days < 0:
                delta += datetime.timedelta(days=1)

            print('Waiting {} seconds for corruption'.format(delta.seconds))
            await asyncio.sleep(delta.seconds)
            await self.corrupt()
            
    @corruptionController.before_loop
    async def before_corruptionController(self):
        print('Waiting...')
        await self.bot.wait_until_ready()
        Data.guild = self.bot.get_guild(Data.guildID)

    @corruptionController.after_loop
    async def on_corruptionController_cancel(self):
        if self.corruptionController.is_being_cancelled() and self.bot.corrupted == True:
            await self.uncorrupt()

    async def corrupt(self):
        self.randomMessage.start()
        #categories = Data.guild.categories
        #Data.chan = await Data.guild.create_text_channel(name='_____',category=random.choice(categories),reason='Error 403: Request Denied')

        try:
            with open('erisGlitch.png', 'rb') as myfile:
                await self.bot.user.edit(username='E̷͑͐r̸̎͝í̴̛s̵', avatar=myfile.read())
        except discord.HTTPException:
            print('Failed to update profile, continuing')
        self.bot.corrupted = True

    async def uncorrupt(self):
        self.randomMessage.cancel()
        await self.disconnect()

        try:
            with open('eris.jpg', 'rb') as myfile:
                await self.bot.user.edit(username='Eris', avatar=myfile.read())
        except discord.HTTPException:
            print('Failed to update profile, continuing')
        self.bot.corrupted = False

    @tasks.loop(minutes=30)
    async def randomMessage(self):
        s = 'HelpMe'
        m = ''.join(random.sample(s, len(s)))
        channels = Data.guild.text_channels
        ch = random.choice(channels)
        message = await ch.send(embed=self.getEmbed(' ', 500))
        Data.mess.append(message)
        for l in m:
            embed = self.getEmbed(l, 500)
            await message.edit(embed=embed)
            await asyncio.sleep(5)

    @randomMessage.after_loop
    async def on_randomMessage_cancel(self):
        if self.randomMessage.is_being_cancelled():
            for m in Data.mess:
                try:
                    await m.delete()
                except discord.HTTPException:
                    print('Message already gone')

    async def disconnect(self):
        voice = get(self.bot.voice_clients, guild=Data.guild)
        if voice and voice.is_connected():
            await voice.disconnect()

    def getEmbed(self, letter: str, length: int):
        d = ''
        for _ in range(0, length):
            c = random.choice(string.ascii_letters)
            if c.lower() == letter.lower():
                d += '**{}** '.format(c)
            else:
                d += '{} '.format(c)
            
        embed = discord.Embed(color=discord.Color(0x33631f), description=d)

        return embed

def setup(bot):
    bot.add_cog(Voice(bot))