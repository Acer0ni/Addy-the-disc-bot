from discord.ext import commands
import requests
from addy.db import Session
from addy.models.coin import Coin


class Crypto(commands.Cog):
    """
    command for finding various data on crypto
    """

    @commands.command(name="coin")
    async def cmd_coin(self, ctx, coin):
        """
        looks up and returns the price of certain crypto currencies
        !coin {coin symbol}
        """
        with Session() as session:
            coin_obj = session.query(Coin).filter_by(symbol=coin).first()
            if not coin_obj:
                await ctx.send("im sorry i cant find that symbol")
                return
        coin_id = coin_obj.coingecko_id
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers)
        response = response.json()
        name = response["name"]
        price = response["market_data"]["current_price"]["usd"]
        await ctx.send(f"The current price of {name} is ${price:,}")
