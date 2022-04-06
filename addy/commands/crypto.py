import requests

from discord.ext import commands
from addy.db import Session
from addy.models import crypto_wallet

from addy.models.coin import Coin
from addy.models.crypto_wallet import Crypto_wallet
from addy.models.crypto_holding import Crypto_holding
from addy.models.transactions import Transaction
from addy.models.user import User

# from addy.models.crypto_wallet import Crypto_wallet
# from addy.models.transactions import Transaction
from enum import Enum


class TransactionType(Enum):
    BUY = True
    SELL = False


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
        await ctx.send(await Crypto.HTTP_helper(coin_id))

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
                user.emptyfavorites()
                await ctx.send("List emptied")
                session.commit()
                return
            session.commit()
            await ctx.send(f"{symbol} deleted")
            await ctx.send(await Crypto.response_formatter(user.favorites))

    @commands.command(name="buycoin")
    async def cmd_buycoin(self, ctx, symbol, amount):
        amount = float(amount)
        with Session() as session:
            user_obj = await Crypto.get_user(session, str(ctx.author))
            coin_obj = session.query(Coin).filter_by(symbol=symbol).first()
            if not coin_obj:
                await ctx.send("I'm sorry i cant find that symbol")
                return
            detailed_coin = await Crypto.get_coin_details(coin_obj.coingecko_id)
            if not detailed_coin:
                await ctx.send(
                    "I am sorry, something went wrong please try again in a few minutes"
                )
            current_price = float(detailed_coin["market_data"]["current_price"]["usd"])
            await ctx.send(f"Current Price: {current_price}")
            wallet = user_obj.crypto_wallet
            new_transaction = Transaction(
                wallet=wallet,
                coin_id=coin_obj.id,
                transaction_type=True,
                amount_transacted=amount,
                coin_price=current_price,
            )
            if new_transaction.total_price > wallet.balance:
                await ctx.send(
                    "I'm sorry you do not have enough money to perform that action"
                )
                return
            wallet.handle_balance(new_transaction)
            holding = (
                session.query(Crypto_holding)
                .filter_by(crypto_wallet_id=wallet.id)
                .filter_by(coingecko_id=coin_obj.coingecko_id)
                .first()
            )
            if not holding:
                holding = Crypto_holding(
                    name=coin_obj.symbol,
                    coingecko_id=coin_obj.coingecko_id,
                    amount=amount,
                    crypto_wallet=wallet,
                )
            else:
                holding.amount += amount
            await ctx.send(wallet.transactions)
            await ctx.send(wallet.crypto_holdings)
            session.commit()
            # await ctx.send(str(new_transaction))

    @commands.command(name="sellcoin")
    async def cmd_sellcoin(self, ctx, symbol, amount):
        amount = float(amount)
        with Session() as session:
            user_obj = await Crypto.get_user(session, str(ctx.author))
            coin_obj = session.query(Coin).filter_by(symbol=symbol).first()
            if not coin_obj:
                await ctx.send("I'm sorry i cant find that symbol")
                return
            detailed_coin = await Crypto.get_coin_details(coin_obj.coingecko_id)
            if not detailed_coin:
                await ctx.send(
                    "I am sorry, something went wrong please try again in a few minutes"
                )
            current_price = float(detailed_coin["market_data"]["current_price"]["usd"])
            wallet = user_obj.crypto_wallet
            holding = (
                session.query(Crypto_holding)
                .filter_by(crypto_wallet_id=wallet.id)
                .filter_by(coingecko_id=coin_obj.coingecko_id)
                .first()
            )
            if not holding:
                await ctx.send(f"I'm sorry you do not have any {coin_obj.name}")
                return
            elif holding.amount < amount:
                await ctx.send(
                    f"you do not have enough {coin_obj.name} to sell {amount}"
                )
                await ctx.send(f"You currently have {holding.amount} {coin_obj.name}")
            new_transaction = Transaction(
                wallet=wallet,
                coin_id=coin_obj.id,
                transaction_type=False,
                amount_transacted=amount,
                coin_price=current_price,
            )
            wallet.handle_balance(new_transaction)
            holding.amount -= amount
            session.commit()

    @commands.command(name="holding")
    async def cmd_show_holding(self, ctx):
        new_line = "\n"
        with Session() as session:
            user_obj = await Crypto.get_user(session, str(ctx.author))
            user_holdings = user_obj.crypto_wallet.crypto_holdings
            response_string = f"{ctx.author} Holdings: {new_line} "

            for holding in user_holdings:
                response_string += str(holding) + "\n"
        await ctx.send(response_string)

    @commands.command(name="transactions")
    async def cmd_show_transactions(self, ctx):
        new_line = "\n"
        with Session() as session:
            user_obj = await Crypto.get_user(session, str(ctx.author))
            user_transaction = user_obj.crypto_wallet.transactions
            response_string = f"{ctx.author} Transactions: {new_line}"

            for transaction in user_transaction:
                response_string += str(transaction) + "\n"
        await ctx.send(response_string)

    async def get_coin_details(id):
        url = f"https://api.coingecko.com/api/v3/coins/{id}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers)
        return response.json()

    async def HTTP_helper(id):
        response = await Crypto.get_coin_details(id)
        name = response["name"]
        price = response["market_data"]["current_price"]["usd"]
        return f"The current price of {name} is ${price:,}"

    async def response_formatter(favorites_list):
        response_string = "Favorites: \n"
        for coin in favorites_list:
            response_string += await Crypto.HTTP_helper(coin.coingecko_id) + "\n"
        return response_string

    async def get_user(session, username):
        user = session.query(User).filter_by(name=username).first()
        if not user:
            wallet = Crypto_wallet()
            user = User(name=username, crypto_wallet=wallet)
            session.commit()
        return user
