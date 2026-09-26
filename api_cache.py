from fastapi import FastAPI
import  requests
from bs4 import BeautifulSoup
import time
app =FastAPI()


#cache storage
cache_data = []
last_fetch = 0

@app.get("/news")
def get_news():
    global cache_data,last_fetch
    start = time.time()
    if time.time()-last_fetch>60:
        # breakpoint()
        print("Fetching new Data")
        url = "https://xyz.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text,"html.parser")
        cache_data=[
            item.text for item in soup.find_all("span",class_="titleline")
        ]
        last_fetch = time.time()
    else:
        print("Using the cache data")
    end = time.time()
    time_taken = round(end-start,4)
    print("Time Taken",time_taken)
    return{
            "Time_Taken":time_taken,
            "data":cache_data[:5]
        }