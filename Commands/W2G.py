import re
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
import json
load_dotenv()

W2G_TOKEN = os.getenv('W2G_TOKEN')
W2G_ROOM = os.getenv('W2G_ROOM')

class Watch2Gether(commands.Cog):
    """
    A suite of commands to help watch videos with friends.
    """
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="create")
    async def W2G_create_room(self,ctx,args):
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
    @commands.command(name='play')
    async def W2G_Play(self,ctx,*args):
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
        if response.status_code == 200:
            await ctx.send("your video is now playing.")
            await ctx.send(f"here is your link https://w2g.tv/rooms/{streamkey}")
        else:
            await ctx.send("something went wrong, please try again.")

    #use *args to make titles optional
    @commands.command(name='add')
    async def W2G_add(self,ctx,streamkey,url,title):
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
        if response.status_code == 200:
            await ctx.send("your video is now queued")
            await ctx.send(f"here is your link https://w2g.tv/rooms/{streamkey}")
        else:
            await ctx.send("something went wrong, please try again.")

