from discord.ext import commands
import requests
import json

skill = [
    "Overall",
    "Attack",
    "Defence",
    "Strength",
    "Constitution",
    "Ranged",
    "Prayer",
    "Magic",
    "Cooking",
    "Woodcutting",
    "Fletching",
    "Fishing",
    "Firemaking",
    "Crafting",
    "Smithing",
    "Mining",
    "Herblore",
    "Agility",
    "Thieving",
    "Slayer",
    "Farming",
    "Runecrafting",
    "Hunter",
    "Construction",
    "Summoning",
    "Dungeoneering",
    "Divination",
    "Invention",
    "Archaeology",
]
activities = [
    "Bounty Hunter",
    "B.H. Rogues",
    "Dominion Tower",
    "The Crucible",
    "Castle Wars games",
    "B.A. Attackers",
    "B.A. Defenders",
    "B.A. Collectors",
    "B.A. Healers",
    "Duel Tournament",
    "Mobilising Armies",
    "Conquest",
    "Fist of Guthix",
    "GG: Athletics",
    "GG: Resource Race",
    "WE2: Armadyl Lifetime Contribution",
    "WE2: Bandos Lifetime Contribution",
    "WE2: Armadyl PvP kills",
    "WE2: Bandos PvP kills",
    "Heist Guard Level",
    "Heist Robber Level",
    "CFP: 5 game average",
    "AF15: Cow Tipping",
    "AF15: Rats killed after the miniquest",
    "RuneScore",
    "Clue Scrolls Easy",
    "Clue Scrolls Medium",
    "Clue Scrolls Hard",
    "Clue Scrolls Elite",
    "Clue Scrolls Master",
]


def highscores_formatter(data):
    f_data = data.split()
    more_f_data = []
    for unit in f_data:
        x = unit.decode("utf-8").split(",")
        more_f_data.append(x)
    return more_f_data


class Runescape(commands.Cog):
    """
    An assortment of Runescape3 functions.
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="hs")
    async def command_HS(self, ctx, *args):
        """
        Use this command to look up a player in RS3.
        """
        username = "{}".format(" ".join(args))
        response = requests.get(
            f"https://secure.runescape.com/m=hiscore/index_lite.ws?player={username}"
        )
        if response.status_code == 404:
            await ctx.send("Sorry, that player is not featured on the Highscores.")
            return
        elif response.status_code != 200:
            await ctx.send("Sorry something went wrong, please try again.")
            return
        formated_response = highscores_formatter(response.content)
        new_line = "\n"
        skill_string = f"**{username}** {new_line}"
        activity_string = ""
        for x in range((len(formated_response))):
            if x < (len(skill) - 1):
                exp = int(formated_response[x][2])
                rank = int(formated_response[x][0])
                skill_string += f"**{skill[x]}** level: {formated_response[x][1]} experience: {exp:,} Rank: {rank:,} {new_line}"
            elif x > (len(skill) - 1):
                rank = int(formated_response[x][0])
                score = int(formated_response[x][1])
                activity_string += f"**{activities[x - (len(skill))]}** Rank: {rank:,} Score: {score:,} {new_line}"
        await ctx.send(skill_string)
        await ctx.send(activity_string)

    @commands.command(name="beast")
    async def cmd_rs3_beast(self, ctx, *args):
        """
        Lets you look up a monster in Runescape3.

        """
        monster = "{}".format(" ".join(args))
        target_monster = await Runescape.beast_search(self, ctx, monster)
        monster_string = await Runescape.beast_stats_formatter(
            self, ctx, target_monster
        )
        await ctx.send(monster_string)

    async def beast_search(self, ctx, monster):
        """
        Takes in the search term and does the blanket search for that term.
        """
        url = f"https://secure.runescape.com/m=itemdb_rs/bestiary/beastSearch.json?term={monster}"
        response = requests.get(url)
        monster = response.json()
        return await Runescape.beast_detail_lookup(self, ctx, monster)

    async def beast_detail_lookup(self, ctx, monster, index=0):
        """
        Attempts to do api call to the specific monster until it finds one suitable.
        """
        id = monster[index]
        url = f"https://secure.runescape.com/m=itemdb_rs/bestiary/beastData.json?beastid={id['value']}"
        response = requests.get(url)
        response = response.json()
        # if "level" not in response:
        #     index = index + 1
        #     return await Runescape.beast_detail_lookup(self, ctx, monster, index)
        # else:
        return response

    async def beast_stats_formatter(self, ctx, monster):
        """
        Takes in the monster dictionary and formats it into a readable string.
        """
        newline = "\n"
        return f"{monster.get('name','N/A')} {newline} Level: {monster.get('level','N/A')}{newline} Lifepoints: {monster.get('lifepoints','N/A')} {newline} Exp: {monster.get('xp','N/A')}{newline} Weakness: {monster.get('weakness','N/A')} {newline} Attack: {monster.get('attack','N/A')}{newline} Defence: {monster.get('defence','N/A')}{newline} Magic: {monster.get('magic','N/A')}{newline} Ranged: {monster.get('ranged','N/A')}{newline} Slayer level: {monster.get('slayerlevel','N/A')}{newline} Slayer category: {monster.get('slayercat','N/A')}{newline} Aggressive: {monster.get('aggressive','N/A')}{newline} Poisonous: {monster.get('poisonous','N/A')}{newline} Examine: {monster.get('description','N/A')}"
