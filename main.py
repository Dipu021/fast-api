from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
users = []
class user(BaseModel):
    name:str
    age:int
    password:str

class userresponse(BaseModel):
    name:str 
    age : int

@app.get("/users",response_model=list[userresponse])
def get_user():
    return users

@app.post("/users")
def create_users(user:user):
     users.append(user)
     return{
         "message":"User Added Successfully"
     }