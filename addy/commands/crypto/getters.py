import requests
from addy.db import Session
from addy.models.crypto_wallet import Crypto_wallet
from addy.models.crypto_holding import Crypto_holding
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
        response_string += f"Name: {coin['name']} Price: {coin['current_price']} Daily change: {coin['price_change_percentage_24h']}%{new_line}"
    return response_string


async def get_user(session, username):
    user = session.query(User).filter_by(name=username).first()
    if not user:
        wallet = Crypto_wallet()
        user = User(name=username, crypto_wallet=wallet)
        session.add(user)
        session.commit()
    if not user.crypto_wallet.id:
        wallet = Crypto_wallet(balance=10000)
        user.crypto_wallet = wallet
        session.commit()
    return user


async def tally_holdings(session, user_obj, user_holdings):

    response = await bulk_http_get(user_holdings)
    holdings_total = 0
    for holding in response:
        current_holding = (
            session.query(Crypto_holding)
            .filter_by(crypto_wallet_id=user_obj.crypto_wallet.id)
            .filter_by(coingecko_id=holding["id"])
            .first()
        )
        holdings_total += holding["current_price"] * current_holding.amount
    return holdings_total


async def amount_calculator(amount, price):
    if amount[0] == "$":
        dollar_amount = float(amount[1:])
        amount = dollar_amount / price
    else:
        amount = float(amount)
    return amount
