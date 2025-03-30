import requests

#pass in an id, and assert that the response is what i expect.
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
    coin_ids = "".join(f"{coin.coingecko_id}," for coin in coin_list)
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin_ids}&order=market_cap_desc&per_page=250&page=1&sparkline=false"
    response = requests.get(url)
    return response.json()

# call bullk http_get before this and just take in that json
async def response_formatter(favorites_list):
    response = await bulk_http_get(favorites_list)
    response_string = "Favorites: \n"
    new_line = "\n"
    for coin in response:
        response_string += f"Name: {coin['name']} Price: ${coin['current_price']:,.2f} Daily change: {coin['price_change_percentage_24h']}%{new_line}"
    return response_string

async def amount_calculator(amount, price):
    if amount[0] == "$":
        dollar_amount = float(amount[1:])
        amount = dollar_amount / price
    else:
        amount = float(amount)
    return amount
