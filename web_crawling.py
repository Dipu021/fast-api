from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/news")
def get_news():
    url = "--------"  #you can put the url of website , remember not every website allow scraping
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")

    title = []

    for item in soup.find_all("--",class_="---------"): # the blank is the xpath of specific field like header or anything
        title.append(item.text)

    return{
        "News":title
    }