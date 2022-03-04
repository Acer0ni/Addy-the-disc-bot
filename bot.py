import os
import random
import discord
import json
from dotenv import load_dotenv
intents = discord.Intents.default()
intents.members = True
intents.presences = True

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
jays_id = 322098392161452033
seans_id = 310226357273493504
COMMAND_CHARACTER = ["!","#"]
count = 1

async def command_99(message):
    """
    Makes me tell you a random Brooklynn 99 quote
    """
    if message.author.id ==  jays_id:
        await message.channel.send("lul nope")
        return
    response = random.choice(brooklyn_99_quotes)
    await message.channel.send(response)

async def command_count(message):
    """
    Returns the amount of times this command has been used since last bot reset
    """
    global count
    await message.channel.send(f'{count}')
    count += 1

async def command_encourage(message):
    """
    responds with a word of encouragement
    """
    with open("Data/encouragement.json") as f:
        encouragement = json.load(f)
    if message.author.id == seans_id:
        await message.channel.send("sorry, nothing nice to say about Canadians")
    response = random.choice(encouragement)
    await message.channel.send(response)

async def command_help(message):
    newline = "\n"
    output = f'Available commands:{newline} !{f"{newline} !".join(list(command_map))}'
    await message.channel.send(output)

async def command_unknown(message):
    await message.channel.send("sorry unknown command")

command_map = {
    '99':command_99,
    'count':command_count,
    'encourage':command_encourage,
    'help':command_help
}
brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} has connect to Discord:\n'
        f'{guild.name}(id: {guild.id})'
        )

@client.event
async def on_member_join(member):
    print("someone joined!")
    # await member.create_dm()
    # await member.dm_channel.send(
    #     f"Hi {member.name}, welcome to my Discord server!"
    # )
    this_guild = member.guild
    print(this_guild.id)
    channel = this_guild.text_channels[0]
    print(channel)
    await channel.send(f"Hi {member.name}, welcome to my Discord server!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!"):
        command = message.content.split()[0][1:]
        await command_map.get(command, command_unknown)(message)
    if message.content == 'raise-exception':
        raise discord.DiscordException


client.run(TOKEN)

