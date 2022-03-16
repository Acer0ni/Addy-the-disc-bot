import os
import discord
import json
from Commands.general import General
from Commands.runescape import Runescape
from Commands.W2g.commands import Watch2Gether
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.presences = True
load_dotenv()
user_data = {}
W2G_TOKEN = os.getenv("W2G_TOKEN")
W2G_ROOM = os.getenv("W2G_ROOM")
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="!", intents=intents)


async def user_loader():
    with open("Data/W2G_Data.json") as json_file:
        data = json.load(json_file)
    return data


@bot.event
async def on_ready():
    Watch2Gether.user_data = await user_loader()
    print(f"{bot.user.name} has connect to Discord:\n")


bot.add_cog(Runescape(bot))
bot.add_cog(General(bot))
bot.add_cog(Watch2Gether(bot))
bot.run(TOKEN)
