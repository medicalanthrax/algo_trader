"""Simulate buying and selling stocks in historical EDGAR data.
Calculate to see if it outperformed the market. Version 1.
"""

import csv
import time
import alpaca
import requests
from tqdm import tqdm
from simulate_buy import simulate_buy_alpaca


def find(data):
    """Find possible trades. Gets all entries in which someone purchases stock.
    :Param data: csv file with entries in read_data() format.
    """
    file = open(data, mode="r", encoding="utf-8", newline="")
    reader = csv.reader(file)

    good_data = []

    for line in reader:
        try:
            if ("P" in line[4] and "none" not in line[1].lower() and "n/a" not in line[1].lower()):
                good_data.append(line)
        except IndexError:
            print("Index Error")
            print(line)
    print(len(good_data))
    return good_data


def buy(amount, file):
    """Simulate buying all possible trades.
    :param file: name of file to search.
    :param amount: float value of buying power.
    :return: Returns percentage gain/loss
    """
    data = find(file)
    amt_for_each = amount/len(data)
    total_profit = 0.0
    for entry in tqdm(data):
        ticker = entry[1][entry[1].find("(")+1:entry[1].find(")")]
        try:
            simulated = simulate_buy_alpaca(ticker, entry[0], 26, amt_for_each)
        except KeyError:
            print(f"KEY ERROR AT {entry}")
            simulated = 0
        except requests.exceptions.HTTPError:
            print(f"HTTPError at {entry}")
        except alpaca.common.exceptions.APIError:
            print(f"API Error at {entry}")
        except requests.exceptions.ConnectionError:
            print("CONNECTION ERROR")
            time.sleep(180)
        except requests.exceptions.ReadTimeout:
            print("TIMEOUT")
            time.sleep(180)
        except TimeoutError:
            print("timeout")
            time.sleep(180)
        except Exception:
            print("general error")
        total_profit += simulated
        print(f"total profit: {total_profit} ")
    print(total_profit)


buy(6706, "2019.csv")
