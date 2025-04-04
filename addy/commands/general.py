from discord.ext import commands
from addy.db import Session
import random
import requests
import json
import datetime, time


count = 1
seans_id = 310226357273493504


class General(commands.Cog):
    """
    A random assortment of commands.
    """

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self} has been loaded")
        global startTime
        startTime = time.time()

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        this_guild = member.guild
        channel = this_guild.text_channels[0]
        await channel.send(f"Hi {member.name}, Welcome to my Discord server!")

    @commands.command(name="uptime")
    async def cmd_uptime(self, ctx):
        """
        Shows how long I have been online for
        """
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))
        await ctx.send(f"I have been online for {uptime}")

    @commands.command(name="count")
    async def command_count(self, ctx):
        """
        Returns the amount of times this command has been used since last bot reset
        """
        global count
        await ctx.send(f"{count}")
        count += 1

    @commands.command(name="encourage")
    async def command_encourage(self, ctx):
        """
        Responds with a word of encouragement
        """
        with open("data/encouragement.json") as f:
            encouragement = json.load(f)
        if ctx.author.id == seans_id:
            await ctx.send("Sorry, nothing nice to say about Canadians.")
            return
        response = random.choice(encouragement)
        await ctx.send(response)

    