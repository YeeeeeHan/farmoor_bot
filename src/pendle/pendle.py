import requests

from config import bot, getChatIdFromEnv
from utils import formatInputForMarkdown

last_check = {
    "yt_eeth_apy": 0,
    "yt_rseth_apy": 0,
    "price_YTeeth": 0,
    "price_YTrseth": 0,
}

PROFILE_MESSAGE = """*_YT eETH_*
APY: {apy_eeth}% \({diff_apy_eeth}% {up_or_down_eeth}\)
Price: {price_YTeeth} \({diff_price_YTeeth}%\)

*_YT rsETH_*
APY: {apy_rseth}% \({diff_apy_rseth}% {up_or_down_rseth}\)
Price: {price_YTrseth} \({diff_price_YTrseth}%\)
"""


def render_up_or_down(value):
    if value > 0:
        return "📈"
    elif value < 0:
        return "📉"
    else:
        return "🔷"


def calculateDifference(new_apy, old_apy):
    difference = new_apy - old_apy
    return round(difference, 3)


def formatPendleMessage(yt_eeth_apy, yt_rseth_apy, price_YTeeth, price_YTrseth):
    return PROFILE_MESSAGE.format(
        apy_eeth=formatInputForMarkdown(yt_eeth_apy),
        diff_apy_eeth=formatInputForMarkdown(calculateDifference(
            yt_eeth_apy, last_check["yt_eeth_apy"])),
        up_or_down_eeth=render_up_or_down(calculateDifference(
            yt_eeth_apy, last_check["yt_eeth_apy"])),
        apy_rseth=formatInputForMarkdown(yt_rseth_apy),
        diff_apy_rseth=formatInputForMarkdown(calculateDifference(
            yt_rseth_apy, last_check["yt_rseth_apy"])),
        up_or_down_rseth=render_up_or_down(calculateDifference(
            yt_rseth_apy, last_check["yt_rseth_apy"])),
        price_YTeeth=formatInputForMarkdown(price_YTeeth),
        diff_price_YTeeth=formatInputForMarkdown(calculateDifference(
            price_YTeeth, last_check["price_YTeeth"])),
        price_YTrseth=formatInputForMarkdown(price_YTrseth),
        diff_price_YTrseth=formatInputForMarkdown(calculateDifference(
            price_YTrseth, last_check["price_YTrseth"])),
    )


def get_pendle_data():
    # Replace with your API endpoint
    url_YTrseth = 'https://api-v2.pendle.finance/core/v1/1/markets/0x4f43c77872db6ba177c270986cd30c3381af37ee'
    url_YTeeth = 'https://api-v2.pendle.finance/core/v1/1/markets/0xf32e58f92e60f4b0a37a69b95d642a471365eae8'
    try:
        # get YT rsEth APY
        response_YTrseth = requests.get(url_YTrseth)
        response_YTrseth.raise_for_status()
        data_YTrseth = response_YTrseth.json()
        yt_rseth_apy = round(data_YTrseth['impliedApy'] * 100, 3)
        yt_rseth_price = round(data_YTrseth['yt']["price"]["acc"], 4)

        # get YT eETH APY
        response_YTeeth = requests.get(url_YTeeth)
        response_YTeeth.raise_for_status()
        data_YTeeth = response_YTeeth.json()
        yt_eeth_apy = round(data_YTeeth['impliedApy'] * 100, 3)
        yt_eeth_price = round(data_YTeeth['yt']["price"]["acc"], 4)

        return yt_eeth_apy, yt_rseth_apy, yt_eeth_price, yt_rseth_price
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")


def price_alert():
    data_YTeeth, data_YTrseth, price_YTeeth, price_YTrseth = get_pendle_data()

    message = formatPendleMessage(
        data_YTeeth, data_YTrseth, price_YTeeth, price_YTrseth)

    if data_YTeeth < 28.5 or data_YTrseth < 28.5:
        bot.send_message(
            getChatIdFromEnv(),
            message,
            parse_mode='MarkdownV2')

        bot.send_message(
            getChatIdFromEnv(),
            formatInputForMarkdown(
                "YT eETH IS LESS THAN 0.285% APY. WE GOT FUCKED BY HEEHAWN. SELL SELL SELL."),
            parse_mode='MarkdownV2')

        bot.send_message(
            getChatIdFromEnv(),
            formatInputForMarkdown(
                "YT rsETH IS LESS THAN 0.285% APY. WE GOT FUCKED BY HEEHAWN. SELL SELL SELL."),
            parse_mode='MarkdownV2')

    if data_YTeeth > 32 or data_YTrseth > 33:
        bot.send_message(
            getChatIdFromEnv(),
            formatInputForMarkdown(message),
            parse_mode='MarkdownV2')

        bot.send_message(
            getChatIdFromEnv(),
            formatInputForMarkdown(
                "YT eETH IS MORE THAN 32% APY. WE ARE WAGMI BECAUSE OF HEEHAWN. TP TP TP."),
            parse_mode='MarkdownV2')

        bot.send_message(
            getChatIdFromEnv(),
            formatInputForMarkdown(
                "YT rsETH IS MORE THAN 33% APY. WE ARE WAGMI BECAUSE OF HEEHAWN. TP TP TP."),
            parse_mode='MarkdownV2')
