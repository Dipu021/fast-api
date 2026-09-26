from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/news")
def get_news(page:int = 1,limit:int = 5):
    url = "https://xyz.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")

    title = []

    for item in soup.find_all("span",class_="titleline"):
        title.append(item.text)
# pagination logic
    start =(page-1)*limit
    end = start+limit

    return{
        "Page":page,
        "Limit":limit,
        "Total":len(title),
        "data":title[start:end]
    }