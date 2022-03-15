import os
import discord
import json
import requests
from Commands.general import General
from Commands.runescape import Runescape
from dotenv import load_dotenv
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.presences = True
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
W2G_TOKEN = os.getenv('W2G_TOKEN')
W2G_ROOM = os.getenv('W2G_ROOM')
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.command(name="create")
async def W2G_create_room(ctx,args):
    """creates a room at watch2gether.tv to watch videos with your friend"""

    share = args
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        "w2g_api_key": W2G_TOKEN,
        "share": share,
        "bg_color": "#00ff00",
        "bg_opacity": "50"
    }
    response = requests.post("https://w2g.tv/rooms/create.json",headers = headers,data=json.dumps(payload))
    content = json.loads(response.content)
    await ctx.send(f"Here is your room! https://w2g.tv/rooms/{content['streamkey']}")
    await ctx.send(f"Please save your room id for future use: {content['streamkey']}")

#refactor this to not use *args (ctx,id,url)
@bot.command(name='play')
async def W2G_Play(ctx,*args):
    """
    plays a video immediately in your chosen room
    !play {room id} {video url}
    """
    streamkey = args[0]
    url = args[1]
    if streamkey == "42":
        streamkey = W2G_ROOM
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        "w2g_api_key": W2G_TOKEN,
        "item_url" : url
    }
    response = requests.post(f"https://w2g.tv/rooms/{streamkey}/sync_update",headers = headers,data=json.dumps(payload))
    await ctx.send("your video is now playing.")
    await ctx.send(f"here is your link https://w2g.tv/rooms/{streamkey}")

#use *args to make titles optional
@bot.command(name='add')
async def W2G_add(ctx,streamkey,url,title):
    """
    add a video to the que of your chosen room
    this feature only works on room created by addy at the moment.
    !add {room id} {video url} {title}
    """
    if streamkey == "42":
        streamkey = W2G_ROOM
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        "w2g_api_key": W2G_TOKEN,
        "add_items": [{"url": url, "title": title}],
    }
    response = requests.post(f"https://w2g.tv/rooms/{streamkey}/playlists/current/playlist_items/sync_update",headers = headers,data=json.dumps(payload))
    await ctx.send("your video is now queued")
    await ctx.send(f"here is your link https://w2g.tv/rooms/{streamkey}")

@bot.event
async def on_ready():
    print(
        f'{bot.user.name} has connect to Discord:\n'

        )

bot.add_cog(Runescape(bot))
bot.add_cog(General(bot))
bot.run(TOKEN)

