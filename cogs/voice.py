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
    corrupted = False
    guildID = 466060673651310593
    guild = None
    chan = None
    mess = []
    startTime = datetime.time(hour=3, minute = 0, second=0)
    endTime = datetime.time(hour=12, minute=0, second=0)

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.corrupt.start()
        self.uncorrupt.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('test')
        #await self.corrupt()
        await asyncio.sleep(300)
        #await self.uncorrupt()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def invade(self, ctx, ch: discord.VoiceChannel):
        """Connect to VC"""
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(ch)
        else:
           voice = await ch.connect()

        _ = os.path.isfile("sound.mp3")
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("sound.mp3"), after=lambda e: print("Sound done!"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        await asyncio.sleep(360)
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

    @tasks.loop(minutes=1)
    async def corrupt(self):
        now = datetime.datetime.now()
        startTime = datetime.datetime.now().replace(hour=Data.startTime.hour, minute=Data.startTime.minute, second=Data.startTime.second)
        endTime = datetime.datetime.now().replace(hour=Data.endTime.hour, minute=Data.endTime.minute, second=Data.endTime.second)
        if Data.corrupted == True:
            delta = startTime - now
            if delta.days < 0:
                delta += datetime.timedelta(days=1)
        else:
            if startTime <= now and endTime > now:
                delta = datetime.timedelta(seconds=0)
            else:
                delta = startTime - now

        print('Waiting {} seconds to corrupt'.format(delta.seconds))
        await asyncio.sleep(delta.seconds)

        #categories = Data.guild.categories
        #Data.chan = await Data.guild.create_text_channel(name='_____',category=random.choice(categories),reason='Error 403: Request Denied')
        self.randomMessage.start()
        with open('erisGlitch.png', 'rb') as myfile:
            await self.bot.user.edit(username='E̷͑͐r̸̎͝í̴̛s̵', avatar=myfile.read())

    @corrupt.before_loop
    async def before_corrupt(self):
        print('Waiting...')
        await self.bot.wait_until_ready()
        Data.guild = self.bot.get_guild(Data.guildID)

    @tasks.loop(minutes=1)
    async def uncorrupt(self):
        if self.bot.user.name != 'Eris':
            Data.corrupted = True
        now = datetime.datetime.now()
        startTime = datetime.datetime.now().replace(hour=Data.startTime.hour, minute=Data.startTime.minute, second=Data.startTime.second)
        endTime = datetime.datetime.now().replace(hour=Data.endTime.hour, minute=Data.endTime.minute, second=Data.endTime.second)
        if Data.corrupted == False:
            delta = endTime - now
            if delta.days < 0:
                delta += datetime.timedelta(days=1)
        else:
            if startTime > now and endTime <= now:
                delta = datetime.timedelta(seconds=0)
            else:
                delta = endTime - now
                if delta.days < 0:
                    delta += datetime.timedelta(days=1)

        print('Waiting {} seconds to uncorrupt'.format(delta.seconds))
        await asyncio.sleep(delta.seconds)

        self.randomMessage.cancel()
        await self.disconnect()
        with open('eris.jpg', 'rb') as myfile:
            await self.bot.user.edit(username='Eris', avatar=myfile.read())

    @uncorrupt.before_loop
    async def before_uncorrupt(self):
        await self.bot.wait_until_ready()
        Data.guild = self.bot.get_guild(Data.guildID)

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
    async def on_randomMessage_canel(self):
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