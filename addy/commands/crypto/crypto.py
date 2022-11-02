import requests

from discord.ext import commands
from addy.db import Session
from addy.models.coin import Coin
import addy.commands.crypto.getters as getters


class Crypto(commands.Cog):
    """
    Command for finding various data on crypto.
    """

    @commands.command(name="coin")
    async def cmd_coin(self, ctx, coin):
        """
        Looks up and returns the price of certain crypto currencies.
        !coin {coin symbol}
        """
        with Session() as session:
            coin_obj = session.query(Coin).filter_by(symbol=coin).first()
            if not coin_obj:
                await ctx.send("I'm sorry, I cant find that symbol.")
                return
        coin_id = coin_obj.coingecko_id
        await ctx.send(await getters.HTTP_helper(coin_id))

    @commands.command(name="addcoin")
    async def cmd_addcoin(self, ctx, symbol):
        """
        Adds a coin to your favorites list.
        !addcoin {coin symbol}
        """
        with Session() as session:
            user = await getters.get_user(session, ctx.author)
            coin_obj = session.query(Coin).filter_by(symbol=symbol).first()
            if not coin_obj:
                await ctx.send("I'm sorry, I cant find that symbol.")
                return
            if coin_obj in user.favorites:
                await ctx.send("That coin is already in your favorites list.")
                return
            user.favorites.append(coin_obj)
            session.add(user)
            session.commit()

            await ctx.send(await getters.response_formatter(user.favorites))

    @commands.command(name="favorites")
    async def cmd_favorites(self, ctx):
        """
        Shows the list of your favorites.
        !favorites
        """
        with Session() as session:
            user = await getters.get_user(session, ctx.author)
            if not user.favorites:
                await ctx.send(
                    "You do not have any favorites yet. You can add favorites by typing !addcoin {coin symbol}"
                )
                return

            await ctx.send(await getters.response_formatter(user.favorites))

    @commands.command(name="delcoin")
    async def cmd_delcoin(self, ctx, symbol):
        """
        Deletes a coin from your favorites list.
        !delcoin {coinsymbol} use "deleteall" to clear favorites list.
        """
        with Session() as session:
            user = await getters.get_user(session, ctx.author)
            new_favorites = [coin for coin in user.favorites if coin.symbol != symbol]
            user.favorites = new_favorites
            if symbol == "deleteall":
                user.emptyfavorites()
                await ctx.send("List emptied")
                session.commit()
                return
            session.commit()
            await ctx.send(f"{symbol} deleted")
