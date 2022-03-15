import os
import discord
import json
import requests
from Commands.general import General
from Commands.runescape import Runescape
from Commands.W2G import Watch2Gether
from dotenv import load_dotenv
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.presences = True
load_dotenv()

W2G_TOKEN = os.getenv('W2G_TOKEN')
W2G_ROOM = os.getenv('W2G_ROOM')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print(
        f'{bot.user.name} has connect to Discord:\n'

        )

bot.add_cog(Runescape(bot))
bot.add_cog(General(bot))
bot.add_cog(Watch2Gether(bot))
bot.run(TOKEN)