import requests

from config import bot, getChatIdFromEnv
from utils import formatInputForMarkdown, pretty_print_numbers

last_check = {
    "current_price": 0,
    "market_cap": 0,
    "fdv": 0,
    "market_cap_fdv_ratio": 0,
}


def render_up_or_down(value):
    if value > 0:
        return "📈"
    elif value < 0:
        return "📉"
    else:
        return "🔷"


def calculatePercentageChange(new, old):
    difference = (new - old)/old
    retVal = round(difference * 100, 3)
    return (retVal, render_up_or_down(retVal))


def formatCoinMessage(id, name, symbol, marketcap, fdv, market_cap_fdv_ratio, currentprice, price_change):
    if currentprice is None:
        currentprice = 0
    if price_change is None:
        price_change = 0
    if marketcap is None:
        marketcap = 0
    if fdv is None:
        fdv = 0
    if market_cap_fdv_ratio is None:
        market_cap_fdv_ratio = 0
    return f"""
*_{name} ${symbol}_*
{"Current Price:":<20}{"$" + pretty_print_numbers(currentprice)}
{"24 Change:":<20}{price_change:.2f}%
{"Market Cap:":<20}{pretty_print_numbers(marketcap)}
{"FDV:":<26}{pretty_print_numbers(fdv)}
{"MC/FDV ratio:":<20}{pretty_print_numbers(market_cap_fdv_ratio*100)} %
"""


def fuzzy_search_coin_id(coin_id):
    url = f'https://api.coingecko.com/api/v3/search?query={coin_id}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if data.get('error') is not None:
        raise (f"{data['error']}")

    return data['coins'][0]['id'], data['coins'][0]['name'], data['coins'][0]['symbol']


def get_coin_data(coin_id):
    id, name, symbol = fuzzy_search_coin_id(coin_id)
    url = f'https://api.coingecko.com/api/v3/coins/{id}'
    response = requests.get(url)
    response.raise_for_status()
    coin_data = response.json()

    if coin_data.get('error') is not None:
        raise (f"{coin_data['error']}")

    if coin_data.get('market_data') is None:
        raise (f"Market data not found for {coin_id}")

    marketcap = 0
    fdv = 0
    market_cap_fdv_ratio = 0
    current_price = 0
    price_change = 0

    if coin_data['market_data'].get("market_cap") is not None:
        marketcap = coin_data['market_data']["market_cap"]["usd"]

    if coin_data['market_data'].get("fully_diluted_valuation") is not None:
        if coin_data['market_data']["fully_diluted_valuation"].get("usd") is not None:
            fdv = coin_data['market_data']["fully_diluted_valuation"]["usd"]

    if coin_data['market_data'].get("market_cap_fdv_ratio") is not None:
        market_cap_fdv_ratio = coin_data['market_data']["market_cap_fdv_ratio"]

    if coin_data['market_data'].get("current_price") is not None:
        if coin_data['market_data']["current_price"].get("usd") is not None:
            current_price = coin_data['market_data']["current_price"]["usd"]
    if coin_data['market_data'].get("price_change_percentage_24h") is not None:
        price_change = coin_data['market_data']["price_change_percentage_24h"]

    return id, name, symbol, marketcap, fdv, market_cap_fdv_ratio, current_price, price_change


# def price_alert():
#     data_YTeeth, data_YTrseth = get_coin_data()

#     message = formatMessage(data_YTeeth, data_YTrseth)

#     if data_YTeeth < 28.5 or data_YTrseth < 28.5:
#         bot.send_message(
#             getChatIdFromEnv(),
#             message,
#             parse_mode='MarkdownV2')

#         bot.send_message(
#             getChatIdFromEnv(),
#             formatInputForMarkdown(
#                 "YT eETH IS LESS THAN 0.285% APY. WE GOT FUCKED BY HEEHAWN. SELL SELL SELL."),
#             parse_mode='MarkdownV2')

#         bot.send_message(
#             getChatIdFromEnv(),
#             formatInputForMarkdown(
#                 "YT rsETH IS LESS THAN 0.285% APY. WE GOT FUCKED BY HEEHAWN. SELL SELL SELL."),
#             parse_mode='MarkdownV2')
