"""For backtesting trading algorithm"""

import datetime
import requests
from ratelimiter import RateLimiter
from alpaca.data.historical import StockHistoricalDataClient


@RateLimiter(max_calls=5, period=60)
def simulate_buy(ticker, date, period, amount, api_key="Y08A7DHDJ0Y1SL4G"):
    """Given stock ticker, simulate profit from buying and holding stock for
    a certain amount of time.
    :param ticker: String object representing the ticker of stock to be
    simulated.
    :param date: String object in YYYY-MM-DD format of date bought
    :param period: Length in weeks to simulate holding the stock
    :param amount: Float object representing the amount you want to buy of
    said stock.
    :param api_key: AlphaVantage API Key
    :return: profit
    """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={ticker}&apikey={api_key}"
    request = requests.get(url=url, timeout=120)
    data = request.json()

    nearest_friday = datetime.date.fromisoformat(date)
    nearest_friday = nearest_friday+datetime.timedelta(days=5-nearest_friday.isoweekday())

    price_at_buy = float(data['Weekly Time Series']
                         [str(nearest_friday)]['4. close'])
    price_at_sell = float(data['Weekly Time Series'][str(
        nearest_friday+datetime.timedelta(weeks=period))]["4. close"])
    return ((price_at_sell/price_at_buy)*amount)-amount

def simulate_buy_alpaca(ticker, date, period, amount):
    """Same as simulate_buy, but using Alpaca API instead of Alphavantage.
    :param ticker: String object representing the ticker of stock to be
    simulated.
    :param date: String object in YYYY-MM-DD format of date bought
    :param period: Length in weeks to simulate holding the stock
    :param amount: Float object representing the amount you want to buy of
    said stock.
    """
    key = "PKUL8J8J58VKUVBXMSLY"
    secret_key = "VX8VmhTirGC0sLrFf1X1TSwGiZ1yVKbfrRskTwWe"
    stock_client = StockHistoricalDataClient(key,secret_key)
    #https://alpaca.markets/docs/python-sdk/market_data.html#market-data