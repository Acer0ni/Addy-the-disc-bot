import os
import random
import discord
import json
from dotenv import load_dotenv
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.presences = True

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
jays_id = 322098392161452033
seans_id = 310226357273493504
count = 1
bot = commands.Bot(command_prefix='!',intents=intents)


@bot.command(name='99')
async def command_99(ctx):
    """
    Makes me tell you a random Brooklynn 99 quote
    """
    if ctx.author.id ==  jays_id:
        await ctx.send("lul nope")
        return
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='count')
async def command_count(ctx):
    """
    Returns the amount of times this command has been used since last bot reset
    """
    global count
    await ctx.send(f'{count}')
    count += 1

@bot.command(name='encourage')
async def command_encourage(ctx):
    """
    responds with a word of encouragement
    """
    with open("Data/encouragement.json") as f:
        encouragement = json.load(f)
    if ctx.author.id == seans_id:
        await ctx.send("sorry, nothing nice to say about Canadians")
    response = random.choice(encouragement)
    await ctx.send(response)

brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

@bot.event
async def on_ready():
    print(
        f'{bot.user.name} has connect to Discord:\n'

        )

@bot.listen()
async def on_member_join(member):
    this_guild = member.guild
    channel = this_guild.text_channels[0]
    await channel.send(f"Hi {member.name}, welcome to my Discord server!")


bot.run(TOKEN)

