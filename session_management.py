from fastapi import FastAPI, Request, Response, status, HTTPException
from typing import Optional

app  = FastAPI()

Users = [{
    "id":1,
    "name":"jack",
    "age":25,
    "city":"pokhara",
    "password":"abc123"
}]

Sessions = {}

@app.post("/login")
async def login(response:Response,request:Request,name:str,password:str):
    for user in Users:
        if user["name"] == name and user["password"]==password:
            session_id = f"{name}_session"
            Sessions[session_id] = {"name":name}
            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True,
                max_age=3600
            )
            return{
                "Message":"Login Successful"
            }
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

# Profile view
@app.get("/profile")
async def get_profile(request:Request):
    session_id : Optional[str]=request.cookies.get("session_id")
    if session_id and session_id in Sessions:
        return{
            "message":f"Welcome {Sessions[session_id]["name"]}"
        }
    raise HTTPException(
        status_code=401,
        detail="Not Authenticated"
    )

# logout

@app.post("/logout")
async def logout(request:Request,response:Response):
    session_id :Optional[str]=request.cookies.get("session_id")
    if session_id and session_id in Sessions:
        del Sessions[session_id]
        response.delete_cookie(key="session_id")
        return{
            "Message":"Logout Successfully"
        }
    raise HTTPException(
        status_code=401,
        detail="Invalid Credentials"
    )