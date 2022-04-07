import requests

from discord.ext import commands
from addy.commands.crypto.getters import Getters
from addy.db import Session
from addy.models.coin import Coin
from addy.models.crypto_wallet import Crypto_wallet
from addy.models.crypto_holding import Crypto_holding
from addy.models.transactions import Transaction
from addy.models.user import User

from enum import Enum


class paperTrading(commands.Cog):
    @commands.command(name="buycoin")
    async def cmd_buycoin(self, ctx, symbol, amount):
        """
        "buys" a crypto coin and adds it to your wallet.
        You start with $10,000. To reset, type !reset
        !buycoin {symbol} {amount}
        """
        amount = float(amount)
        with Session() as session:
            user_obj = await Getters.get_user(session, str(ctx.author))
            coin_obj = session.query(Coin).filter_by(symbol=symbol).first()
            if not coin_obj:
                await ctx.send("I'm sorry, I cant find that symbol.")
                return
            detailed_coin = await Getters.get_coin_details(coin_obj.coingecko_id)
            if not detailed_coin:
                await ctx.send(
                    "I'm sorry, something went wrong. Please try again in a few minutes."
                )
            current_price = float(detailed_coin["market_data"]["current_price"]["usd"])
            wallet = user_obj.crypto_wallet
            new_transaction = Transaction(
                wallet=wallet,
                coin_id=coin_obj.id,
                is_sale=True,
                amount_transacted=amount,
                coin_price=current_price,
            )
            if new_transaction.total_price > wallet.balance:
                await ctx.send(
                    "I'm sorry, you do not have enough money to perform that action."
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
            await ctx.send(holding)
            session.commit()

    @commands.command(name="sellcoin")
    async def cmd_sellcoin(self, ctx, symbol, amount):
        """
        Sells a coin from your wallet.
        Type !reset to reset your wallet and transactions.
        !sellcoin {symbol} {amount}
        """
        amount = float(amount)
        with Session() as session:
            user_obj = await Getters.get_user(session, str(ctx.author))
            coin_obj = session.query(Coin).filter_by(symbol=symbol).first()
            if not coin_obj:
                await ctx.send("I'm sorry, I cant find that symbol.")
                return
            detailed_coin = await Getters.get_coin_details(coin_obj.coingecko_id)
            if not detailed_coin:
                await ctx.send(
                    "I'm sorry, something went wrong. Please try again in a few minutes."
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
                await ctx.send(f"I'm sorry, you do not have any {coin_obj.name}")
                return
            elif holding.amount < amount:
                await ctx.send(
                    f"You do not have enough {coin_obj.name} to sell {amount}"
                )
                await ctx.send(f"You currently have {holding.amount} {coin_obj.name}")
            new_transaction = Transaction(
                wallet=wallet,
                coin_id=coin_obj.id,
                is_sale=False,
                amount_transacted=amount,
                coin_price=current_price,
            )
            wallet.handle_balance(new_transaction)
            holding.amount -= amount
            if holding.amount == 0:
                print("out of this coin")
            session.commit()
            await ctx.send(holding)

    @commands.command(name="wallet")
    async def cmd_show_holding(self, ctx):
        """
        Shows the users holdings and balance.
        !wallet
        """
        new_line = "\n"
        with Session() as session:
            user_obj = await Getters.get_user(session, str(ctx.author))
            user_holdings = (
                session.query(Crypto_holding)
                .filter(
                    Crypto_holding.amount > 0,
                    Crypto_holding.crypto_wallet_id == user_obj.crypto_wallet.id,
                )
                .all()
            )
            if not user_holdings:
                await ctx.send(
                    f"Balance: {user_obj.crypto_wallet.balance}{new_line} You currently do not have any holdings."
                )
                return
            holding_total = await Getters.tally_holdings(
                self, session, user_obj, user_holdings
            )
            response_string = f"{ctx.author}{new_line}Balance: ${user_obj.crypto_wallet.balance}{new_line}Holdings: {new_line}Total value: ${holding_total}{new_line}"

            for holding in user_holdings:
                response_string += str(holding) + "\n"
        await ctx.send(response_string)

    @commands.command(name="transactions")
    async def cmd_show_transactions(self, ctx):
        """
        Shows the users transactions.
        !transactions
        """
        new_line = "\n"
        with Session() as session:
            user_obj = await Getters.get_user(session, str(ctx.author))
            user_transaction = user_obj.crypto_wallet.transactions
            response_string = f"{ctx.author} Transactions: {new_line}"

            for transaction in user_transaction:
                response_string += str(transaction) + "\n"
        await ctx.send(response_string)

    @commands.command(name="reset")
    async def cmd_reset(self, ctx):
        """
        Resets your crypto wallet.
        !reset
        """
        with Session() as session:
            user_obj = await Getters.get_user(session, str(ctx.author))
            new_wallet = Crypto_wallet()
            user_obj.crypto_wallet = new_wallet
            session.commit()
            await ctx.send("Deletion successful")