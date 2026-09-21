from fastapi import FastAPI,Depends,Header,HTTPException
from jose import jwt
from datetime import datetime,timedelta,timezone

app = FastAPI()
SECRECT_KEY = "secretkey"
ALGORITHM = "HS256"


# First create the token

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=30)
    to_encode.update({
        "exp":expire
    })
    token = jwt.encode(to_encode,SECRECT_KEY,algorithm=ALGORITHM)
    return token

# Login Api/ Token generation
@app.post("/login")
def login(username:str,password:str):
    if username!="admin" or password!="1234":
        raise HTTPException(
            status_code=401,
            detail="Invaid Username OR password"
        )
    token=create_token({
        "sub":username
    })
    return{
        "Message":"Successfully Genareted the token",
        "access_token":token
    }

# Token Verification
def verify_token(token:str=Header(None)):
    try:
        payload = jwt.decode(token,SECRECT_KEY,algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token or Token Expired"
        )

# Protected Route
@app.get("/secure")
def secure(user=Depends(verify_token)):
    return{
        "Message":"Secured Data Accessed",
        "user":user
    }
