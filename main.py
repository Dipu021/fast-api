from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class users(BaseModel):
    name:str
    age:int
    password:str

class userresponse(BaseModel):
    name:str 
    age : int

@app.get("/users",response_model=userresponse)
def get_user():
    return{
        "name":"John",
        "age":23,
        "password":"123456"
    }