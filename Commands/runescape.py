from discord.ext import commands
import requests
import json

skill = ['Overall','Attack', 'Defence', 'Strength', 'Constitution', 'Ranged', 'Prayer', 'Magic', 'Cooking', 'Woodcutting', 'Fletching', 'Fishing', 'Firemaking', 'Crafting', 'Smithing', 'Mining', 'Herblore', 'Agility', 'Thieving', 'Slayer', 'Farming', 'Runecrafting', 'Hunter', 'Construction', 'Summoning', 'Dungeoneering', 'Divination', 'Invention', 'Archaeology']
activities = ['Bounty Hunter','B.H. Rogues','Dominion Tower','The Crucible','Castle Wars games', 'B.A. Attackers', 'B.A. Defenders', 'B.A. Collectors','B.A. Healers', 'Duel Tournament','Mobilising Armies','Conquest','Fist of Guthix','GG: Athletics','GG: Resource Race','WE2: Armadyl Lifetime Contribution','WE2: Bandos Lifetime Contribution','WE2: Armadyl PvP kills','WE2: Bandos PvP kills','Heist Guard Level','Heist Robber Level','CFP: 5 game average','AF15: Cow Tipping','AF15: Rats killed after the miniquest','RuneScore', 'Clue Scrolls Easy','Clue Scrolls Medium','Clue Scrolls Hard','Clue Scrolls Elite','Clue Scrolls Master']


def highscores_formatter(data):
    f_data = data.split()
    more_f_data =[] 
    for unit in f_data:
        x = unit.decode('utf-8').split(',')
        more_f_data.append(x)
    return more_f_data

class Runescape(commands.Cog):
    """
    An assortment of Runescape3 functions.
    """
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

   

    @commands.command(name='hs')
    async def command_HS(self,ctx,*args):
        """
        Use this command to look up a player in RS3.
        """
        username = '{}'.format(' '.join(args))
        response = requests.get(f"https://secure.runescape.com/m=hiscore/index_lite.ws?player={username}")
        if response.status_code == 404:
            await ctx.send("Sorry, that player is not featured on the Highscores.")
            return
        elif response.status_code != 200:
            await ctx.send("Sorry something went wrong, please try again. ")
            return
        formated_response = highscores_formatter(response.content)
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
    