import requests
from addy.db import Session
from addy.models import historicalwalletvalue
from addy.models.crypto_wallet import Crypto_wallet
from addy.models.crypto_holding import Crypto_holding
from addy.models.historicalwalletvalue import HistoricalWalletValue
from addy.models.user import User


async def get_coin_details(id):
    url = f"https://api.coingecko.com/api/v3/coins/{id}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers)
    return response.json()


async def HTTP_helper(id):
    response = await get_coin_details(id)
    name = response["name"]
    price = response["market_data"]["current_price"]["usd"]
    return f"The current price of {name} is ${price:,}"


async def bulk_http_get(coin_list):
    if len(coin_list) == 0:
        print("no coin list in bulk http get")
        return None
    coin_ids = ""
    for coin in coin_list:
        coin_ids += f"{coin.coingecko_id},"
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin_ids}&order=market_cap_desc&per_page=250&page=1&sparkline=false"
    response = requests.get(url)
    return response.json()


async def response_formatter(favorites_list):
    response = await bulk_http_get(favorites_list)
    response_string = "Favorites: \n"
    new_line = "\n"
    for coin in response:
        response_string += f"Name: {coin['name']} Price: ${coin['current_price']:,.2f} Daily change: {coin['price_change_percentage_24h']}%{new_line}"
    return response_string


# this is too big and complicated, figure out how to fix it.
async def get_user(session, username):
    user = session.query(User).filter_by(name=username).first()

    if not user:
        print("hi mom")
        user = User(name=username)
        session.add(user)
        session.commit()
    if not user.crypto_wallet:
        wallet = Crypto_wallet()
        session.add(wallet)
        user.crypto_wallet = wallet
        session.flush()
        holding_total = await tally_holdings(
            session, user, user.crypto_wallet.crypto_holdings
        )

        print(wallet)
        new_hwallet_value = HistoricalWalletValue(
            crypto_wallet_id=user.crypto_wallet.id,
            usd_balance=user.crypto_wallet.balance,
            holdings_balance=holding_total,
            total_balance=holding_total + user.crypto_wallet.balance,
        )
        wallet.historicalvalue.append(new_hwallet_value)

        session.commit()
    return user


async def tally_holdings(session, user_obj, user_holdings):

    response = await bulk_http_get(user_holdings)
    holdings_results = {
        "total": 0,
        "coins": {},
    }
    if not response:
        print("no holdings in tally holdings")
        return holdings_results
    for holding in response:
        current_holding = (
            session.query(Crypto_holding)
            .filter_by(crypto_wallet_id=user_obj.crypto_wallet.id)
            .filter_by(coingecko_id=holding["id"])
            .first()
        )
        holdings_results["coins"][current_holding.coingecko_id] = {
            "amount": current_holding.amount,
            "value": holding["current_price"],
        }
        holdings_results["total"] += holding["current_price"] * current_holding.amount
    return holdings_results


async def amount_calculator(amount, price):
    if amount[0] == "$":
        dollar_amount = float(amount[1:])
        amount = dollar_amount / price
    else:
        amount = float(amount)
    return amount
