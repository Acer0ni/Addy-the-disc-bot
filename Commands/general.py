from discord.ext import commands
import discord
import random
import json
import requests

count = 1
seans_id = 310226357273493504
jays_id = 322098392161452033


class General(commands.Cog):
    """
    A random assortment of commands.
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        this_guild = member.guild
        channel = this_guild.text_channels[0]
        await channel.send(f"Hi {member.name}, Welcome to my Discord server!")

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
        with open("Data/encouragement.json") as f:
            encouragement = json.load(f)
        if ctx.author.id == seans_id:
            await ctx.send("Sorry, nothing nice to say about Canadians.")
            return
        response = random.choice(encouragement)
        await ctx.send(response)

    @commands.command(name="99")
    async def command_99(self, ctx):
        """
        Makes me tell you a random Brooklynn 99 quote
        """
        if ctx.author.id == jays_id:
            await ctx.send("lul nope")
            return
        response = requests.get(
            "https://brooklyn-nine-nine-quotes.herokuapp.com/api/v1/quotes/random"
        )
        content = json.loads(response.content)
        await ctx.send(content["Data"]["QuoteText"])
