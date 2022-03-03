import os
import random
import discord
import json
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
jays_id = 322098392161452033
seans_id = 310226357273493504
client = discord.Client()
count = 0
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
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, welcome to my Discord server!"
    )
    print("it worked!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # elif message.author.id ==  jays_id:
    #     print("jay is typing")
    #     await message.channel.send("you suck jay")
    #     return
    print(message.author)
    global count
    with open("Data/encouragement.json") as f:
        encouragement = json.load(f)
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '!99':
        if message.author.id ==  jays_id:
            await message.channel.send("lul nope")
            return
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    elif message.content == '!count':
        await message.channel.send(f'{count}')
        count += 1
    elif message.content =='!encourage':
        if message.author.id == seans_id:
            await message.channel.send("sorry, nothing nice to say about Canadians")
        response = random.choice(encouragement)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException
# class CustomClient(discord.Client):
#     async def on_ready(self):
#         print(f'{self.user} has connected to discord!')
    

# client = CustomClient()    
client.run(TOKEN)

