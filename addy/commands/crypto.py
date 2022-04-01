from poplib import CR
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
        await ctx.send(Crypto.HTTP_helper(coin_id))

    @commands.command(name="addcoin")
    async def cmd_addcoin(self, ctx, symbol):
        """
        adds a coin to your favorites list
        !addcoin {coin symbol}
        """
        with Session() as session:
            user = await Crypto.get_user(session, str(ctx.author))
            coin_obj = session.query(Coin).filter_by(symbol=symbol).first()
            if not coin_obj:
                await ctx.send("I'm sorry i cant find that symbol")
                return
            if coin_obj in user.favorites:
                await ctx.send("That coin is already in your favorites list")
                return
            user.favorites.append(coin_obj)
            session.add(user)
            session.commit()

            await ctx.send(await Crypto.response_formatter(user.favorites))

    @commands.command(name="favorites")
    async def cmd_favorites(self, ctx):
        """
        shows the list of your favorites
        !favorites
        """
        with Session() as session:
            user = await Crypto.get_user(session, str(ctx.author))
            if not user.favorites:
                await ctx.send(
                    "you do not have any favorites yet. you can add favorites by typing !addcoin {coin symbol}"
                )
                return

            await ctx.send(await Crypto.response_formatter(user.favorites))

    @commands.command(name="delcoin")
    async def cmd_delcoin(self, ctx, symbol):
        """
        Deletes a coin from your favorites list.
        !delcoin {coinsymbol} use "deleteall" to clear favorites list.
        """
        with Session() as session:
            user = await Crypto.get_user(session, str(ctx.author))
            new_favorites = [coin for coin in user.favorites if coin.symbol != symbol]
            user.favorites = new_favorites
            if symbol == "deleteall":
                user.favorites = []
            session.commit()
            await ctx.send(await Crypto.response_formatter(user.favorites))

    async def HTTP_helper(id):
        url = f"https://api.coingecko.com/api/v3/coins/{id}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers)
        response = response.json()
        name = response["name"]
        price = response["market_data"]["current_price"]["usd"]
        return f"The current price of {name} is ${price:,}"

    async def response_formatter(favorites_list):
        response_string = "Favorites: \n"
        for coin in favorites_list:
            response_string += await Crypto.HTTP_helper(coin.coingecko_id) + "\n"
        return response_string

    async def get_user(session, username):
        return session.query(User).filter_by(name=username).first() or User(
            name=username
        )
