from cmath import exp
import os
import random
from unicodedata import category
import discord
import json
import requests
from dotenv import load_dotenv
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.presences = True

load_dotenv()
skill = ['Overall','Attack', 'Defence', 'Strength', 'Constitution', 'Ranged', 'Prayer', 'Magic', 'Cooking', 'Woodcutting', 'Fletching', 'Fishing', 'Firemaking', 'Crafting', 'Smithing', 'Mining', 'Herblore', 'Agility', 'Thieving', 'Slayer', 'Farming', 'Runecrafting', 'Hunter', 'Construction', 'Summoning', 'Dungeoneering', 'Divination', 'Invention', 'Archaeology']
activities = ['Bounty Hunter','B.H. Rogues','Dominion Tower','The Crucible','Castle Wars games', 'B.A. Attackers', 'B.A. Defenders', 'B.A. Collectors','B.A. Healers', 'Duel Tournament','Mobilising Armies','Conquest','Fist of Guthix','GG: Athletics','GG: Resource Race','WE2: Armadyl Lifetime Contribution','WE2: Bandos Lifetime Contribution','WE2: Armadyl PvP kills','WE2: Bandos PvP kills','Heist Guard Level','Heist Robber Level','CFP: 5 game average','AF15: Cow Tipping','AF15: Rats killed after the miniquest','RuneScore', 'Clue Scrolls Easy','Clue Scrolls Medium','Clue Scrolls Hard','Clue Scrolls Elite','Clue Scrolls Master']
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
jays_id = 322098392161452033
seans_id = 310226357273493504
count = 1
bot = commands.Bot(command_prefix='!',intents=intents)

#deal with multi word names
@bot.command(name='hs',category ='runescape')
async def command_HS(ctx,*args):
    """
    use this command to look up a player in RS3
    """
    username = '{}'.format(' '.join(args))
    response = requests.get(f"https://secure.runescape.com/m=hiscore/index_lite.ws?player={username}")
    if response.status_code == 404:
        await ctx.send("sorry that player is not featured on the Highscores")
        return
    elif response.status_code != 200:
        await ctx.send("sorry something went wrong, please try again")
        return
    formated_response =highscores_formatter(response.content)
    new_line= '\n'
    skill_string = f"**{username}** {new_line}"
    activity_string =""
    for x in range((len(formated_response))):
        if x < (len(skill) -1):
            exp=int(formated_response[x][2])
            rank=int(formated_response[x][0])
            skill_string += f"**{skill[x]}** level: {formated_response[x][1]} experience: {exp:,} Rank: {rank:,} {new_line}"
        elif x > (len(skill) - 1):
            rank = int(formated_response[x][0])
            score = int(formated_response[x][1])
            activity_string += f"**{activities[x - (len(skill))]}** Rank: {rank:,} Score: {score:,} {new_line}"
    await ctx.send(skill_string)
    await ctx.send(activity_string)

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
        return
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

def highscores_formatter(data):
    f_data = data.split()
    more_f_data =[] 
    for unit in f_data:
        x = unit.decode('utf-8').split(',')
        more_f_data.append(x)
    return more_f_data

bot.run(TOKEN)

