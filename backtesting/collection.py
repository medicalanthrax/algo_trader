"""Get all the xml form 4 files from a given year.
Create a csv file and put them all in, sorted by date.
"""
import sys
import requests
import time
sys.path.insert(0,"C:\\Users\\carlo\\coding\\algo_trader\\EDGAR_Scraper")
from read_data import read_data

def collection(year):
    """Get all the xml form 4 files from given year"""
    good_data = []
    for quarter in range(1,5):        #For each of the four quarters
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

    good_data.sort(key= my_func)
    print("sorted")

    for idx,line in enumerate(good_data):              #Get only the dir links from each entry.
        good_data[idx] = f"https://www.sec.gov/Archives/{line[98:].replace(' ','')}"

    return good_data

collected = collection(2017)
start = time.perf_counter()
for i in collected[0:100]:
    print(read_data(i))
end = time.perf_counter()
print(f"time elapsed: {end-start}")
