import os
import discord
import json
import requests
from Commands.general import General
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
W2G_TOKEN = os.getenv('W2G_TOKEN')
W2G_ROOM = os.getenv('W2G_ROOM')
bot = commands.Bot(command_prefix='!',intents=intents)


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

def highscores_formatter(data):
    f_data = data.split()
    more_f_data =[] 
    for unit in f_data:
        x = unit.decode('utf-8').split(',')
        more_f_data.append(x)
    return more_f_data
bot.add_cog(General(bot))
bot.run(TOKEN)

