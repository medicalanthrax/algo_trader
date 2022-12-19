"""Simulate buying and selling stocks in historical EDGAR data.
Calculate to see if it outperformed the market. Version 1.
"""
import csv

def find(data):
    """Find possible trades. Gets all entries in which someone purchases stock.
    :Param data: csv file with entries in read_data() format.
    """
    file = open(data,mode="r", encoding="utf-8",newline="")
    reader = csv.reader(file)

    good_data = []

    for line in reader:
        try:
            if "P" in line[4]:
                good_data.append(line)
        except IndexError:
            print("Index Error")
            print(line)
    return good_data
print(len(find("2019.csv")))
