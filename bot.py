import os
from pathlib import Path
import discord
import json
import asyncio

from requests import Session
from sqlalchemy import null
from addy.commands.general import General
from addy.db import Session
from addy.commands.runescape import Runescape
from addy.commands.crypto.crypto import Crypto
from addy.models.user import User
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

async def seed_users():
    discord_users = list(bot.get_all_members())
    with Session() as session:
        db_users = session.query(User).all()
        for db_user in db_users:
            for discord_user in discord_users:
                if db_user.name == str(discord_user):
                    print(f"db_name {db_user.name} disc name {str(discord_user)}")
                    db_user.discord_id = discord_user.id
                    session.commit()
                    




@bot.event
async def on_ready():
    now = datetime.now()
    await seed_users()
    General.start_time = now.strftime("%H:%M:%S")
    print(f"{bot.user.name} has connect to Discord:\n")

async def setup(bot):
    await bot.add_cog(Runescape(bot))
    await bot.add_cog(General(bot))
    await bot.add_cog(Crypto(bot))

asyncio.run(setup(bot))
bot.run(TOKEN)
