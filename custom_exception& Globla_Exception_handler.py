from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse

app = FastAPI()

class usernotfoundexception(Exception):
    def __init__(self,name:str):
        self.name = name

@app.exception_handler(usernotfoundexception)
def user_not_found_handler(request = Request,exc = usernotfoundexception):
    return JSONResponse(
        status_code=404,
        content={
            "Status":"Error",
            "message":f"User {exc.name} Not Found"
        }
    )

@app.get("/user/{name}")
def get_user(name:str):
    if name != "John":
        raise usernotfoundexception(name)
    return{
        "Message":"Successful Retrival",
        "Name":"John"
    }
