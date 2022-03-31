from discord.ext import commands
import requests
from addy.db import Session
from addy.models.coin import Coin
from addy.models.user import User


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

    @commands.command(name="addcoin")
    async def cmd_addcoin(self, ctx, symbol):
        with Session() as session:
            user = session.query(User).filter_by(name=str(ctx.author)).first()
            if not user:
                user = User(name=str(ctx.author))
                session.flush()
            coin_obj = session.query(Coin).filter_by(symbol=symbol).first()
            if not coin_obj:
                await ctx.send("im sorry i cant find that symbol")
                return
            user.favorites.append(coin_obj)
            session.add(user)
            session.commit()
            for coin in user.favorites:
                await ctx.send(Crypto.HTTP_helper(coin.symbol))

    async def HTTP_helper(id):

        url = f"https://api.coingecko.com/api/v3/coins/{id}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers)
        response = response.json()
        name = response["name"]
        price = response["market_data"]["current_price"]["usd"]
        return f"The current price of {name} is ${price:,}"