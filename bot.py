import os
from pathlib import Path
import discord
import json
import asyncio
from addy.commands.general import General
from addy.commands.runescape import Runescape
from addy.commands.w2g.commands import Watch2Gether
from addy.commands.crypto.crypto import Crypto
from addy.commands.crypto.paper_trading import paperTrading
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.all()
load_dotenv()
user_data = {}
W2G_TOKEN = os.getenv("W2G_TOKEN")
W2G_ROOM = os.getenv("W2G_ROOM")
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
COMMAND_PREFIX = os.getenv("ADDY_COMMAND_PREFIX", "!")

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


async def user_loader():
    data_file = Path("./data/W2G_users.json")
    if not data_file.is_file():
        data_file.write_text("{}")
    with open("data/W2G_users.json") as json_file:
        data = json.load(json_file)
    return data


@bot.event
async def on_ready():
    Watch2Gether.user_data = await user_loader()
    now = datetime.now()
    General.start_time = now.strftime("%H:%M:%S")
    print(f"{bot.user.name} has connect to Discord:\n")

async def setup(bot):
    await bot.add_cog(Runescape(bot))
    await bot.add_cog(General(bot))
    await bot.add_cog(paperTrading(bot))
    await bot.add_cog(Watch2Gether(bot))
    await bot.add_cog(Crypto(bot))

asyncio.run(setup(bot))
bot.run(TOKEN)
