import requests
from addy.models.coin import Coin
from db import engine as db


def seed_coin():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    response = response.json()
    for coin in response:
        new_coin = Coin(
            name=coin["name"], symbol=coin["symbol"], coingecko_id=coin["id"]
        )
        db.session.add(new_coin)
    db.session.commit()
    print("seed completed")
