import requests
from addy.models.coin import Coin
from addy.db import Session


def seed_coin():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    response = response.json()
    with Session.begin() as session:
        for coin in response:
            new_coin = Coin(
                name=coin["name"], symbol=coin["symbol"], coingecko_id=coin["id"]
            )
            session.add(new_coin)

    print("seed completed")
