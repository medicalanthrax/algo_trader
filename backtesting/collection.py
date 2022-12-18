"""Get all the xml form 4 files from a given year.
Create a csv file and put them all in, sorted by date.
"""
import csv
import multiprocessing
import sys

import requests
from tqdm import tqdm
from ratelimiter import RateLimiter

# sys.path.insert(0, "C:\\Users\\carlo\\coding\\algo_trader\\EDGAR_Scraper")
sys.path.insert(0, "C:\\Users\\User\\Code\\EDGAR_scraper\\EDGAR-Database-Insider-Trading-Tracker")
from read_data import read_data  # pylint: disable= import_error  #pylint: disable= wrong-import-position


def collection(year):
    """Get all the xml form 4 files from given year"""
    good_data = []
    for quarter in range(1, 5):  # For each of the four quarters
        url = f"https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{quarter}/form.idx"
        request = requests.get(
            url, headers={"User-Agent": "Carlo Tran carlotran4@gmail.com"}, timeout=30)
        data = request.text.split("\n")

        for j in data[0:-1]:
            if j[0] == "4" and j[1] == " ":
                good_data.append(j)
    print("collected all data")

    def my_func(e):
        return e[91:96]

    good_data.sort(key=my_func)
    print("sorted")

    # Get only the dir links from each entry.
    for idx, line in enumerate(good_data):
        good_data[idx] = f"https://www.sec.gov/Archives/{line[98:].replace(' ','')}"

    return good_data


def write_to_csv(year):
    """Using collection() and read_data(),
    write new csv file in directory with all data collected from year.
    """
    if __name__ == "__main__":
        with multiprocessing.Manager() as manager:
            collected = collection(year)
            first_half = manager.list(collected[0:int(len(collected)/2)])
            second_half = manager.list(collected[int(len(collected)/2):])
            # first_half = manager.list(collected[0:100])
            # second_half = manager.list(collected[100:200])
            p1 = multiprocessing.Process(target = get_data, args = (first_half,))
            p2 = multiprocessing.Process(target=get_data, args= (second_half,))

            p1.start()
            p2.start()

            p1.join()
            p2.join()

            file = open(f"{year}.csv",mode="w",encoding="utf-8", newline="")
            my_writer = csv.writer(file,delimiter=",")
            for i in first_half:
                my_writer.writerow(i)
            for i in second_half:
                my_writer.writerow(i)
def get_data(file_link_list):
    """Given list of links to EDGAR form 4 xml files, mutate into list of data.
    No return.
    """
    for idx,i in tqdm(enumerate(file_link_list)):
        file_link_list[idx] = read_data(i)
    print(len(file_link_list))

write_to_csv(2019)
