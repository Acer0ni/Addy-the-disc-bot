from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
import json
from Commands.w2g.http import W2G_helper

load_dotenv()
# why did this suddenly change from a dict to a sub routine when i moved it
# user_data = user_data
W2G_TOKEN = os.getenv("W2G_TOKEN")
W2G_ROOM = os.getenv("W2G_ROOM")


class Watch2Gether(commands.Cog):
    """
    A suite of commands to help watch videos with friends.
    """

    user_data = {}

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="create")
    async def CMD_W2G_create_room(self, ctx, url):
        """
        Creates a room at watch2gether.tv to watch videos with your friends.
        """
        author = str(ctx.message.author)

        if author in self.user_data:
            await ctx.send(
                f"You already have a room created. Your url is https://w2g.tv/rooms/{self.user_data[author]} "
            )
            return
        streamkey = await W2G_helper.W2G_create_room(url)
        if not streamkey:
            await ctx.send("Something went wrong, please try again.")
        else:
            await ctx.send(f"Here is your room! https://w2g.tv/rooms/{streamkey}")
            self.user_data[author] = streamkey
            json_string = json.dumps(self.user_data)
            with open("Data/W2G_data.json", "w") as outfile:
                outfile.write(json_string)

    @commands.command(name="play")
    async def CMD_W2G_Play(self, ctx, url):
        """
        Plays a video immediately in your personal room, and will create one for you if you don't have one.
        !play {video url}
        """
        author = str(ctx.message.author)
        if author not in self.user_data:
            await Watch2Gether.CMD_W2G_create_room(self, ctx, url)
            return
        response = await W2G_helper.W2G_play(self.user_data[author], url)
        if response == 200:
            await ctx.send("Your video is now playing.")
            await ctx.send(
                f"Here is your link! https://w2g.tv/rooms/{self.user_data[author]}"
            )
        elif response == 403:
            streamkey = await W2G_helper.W2G_create_room(url)
            if not streamkey:
                await ctx.send(
                    "something went wrong with room creation, the api may be down please try again later"
                )
            self.user_data[author] = streamkey
            json_string = json.dumps(self.user_data)
            with open("Data/W2G_data.json", "w") as outfile:
                outfile.write(json_string)
            await ctx.send(
                "something went wrong interacting with your old room, this usually happens because it was not saved and over 24 hours have passed since it was last used."
            )
            await ctx.send(
                f"we made a new room for you. here is your link: https://w2g.tv/rooms/{streamkey}"
            )

        else:
            await ctx.send("Something went wrong, please try again.")

    @commands.command(name="add")
    async def CMD_W2G_add(self, ctx, url, title="none"):
        """
        Add a video to the queue of your personal room. If you do not have a room,it creates one and plays the video for you.
        !add {video url} {title}(optional)
        """
        author = str(ctx.message.author)
        if author not in self.user_data:
            await Watch2Gether.CMD_W2G_create_room(self, ctx, url)
            return
        response = await W2G_helper.W2G_add(self.user_data[author], url, title)

        if response == 200:
            await ctx.send("Your video is now queued.")
            await ctx.send(
                f"Here is your link! https://w2g.tv/rooms/{self.user_data[author]}"
            )
        elif response == 403:
            streamkey = await W2G_helper.W2G_create_room(url)
            if not streamkey:
                await ctx.send(
                    "something went wrong with room creation, the api may be down please try again later"
                )
            self.user_data[author] = streamkey
            json_string = json.dumps(self.user_data)
            with open("Data/W2G_data.json", "w") as outfile:
                outfile.write(json_string)
            await ctx.send(
                "something went wrong interacting with your old room, this usually happens because it was not saved and over 24 hours have passed since it was last used."
            )
            await ctx.send(
                f"we made a new room for you. here is your link: https://w2g.tv/rooms/{streamkey}"
            )
        else:
            print(response)
            await ctx.send("Something went wrong, please try again.")
