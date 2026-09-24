from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return{
        "message":"Hello! Welcome back"
    }

@app.get("/add")
def add(a:int,b:int):
    return{
        "sum":a+b
    }
