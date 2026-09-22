from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta,timezone
from passlib.context import CryptContext
from jose import jwt

#FastAPI Setup
app = FastAPI()

# JWT Configuration
SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hashing Setup
pwd_context = CryptContext(schemes=["bcrypt"])

# OAuth Setup
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

# Dummy UserDB
fake_user_db = {
    "admin":{
        "username":"admin",
        "hashed_password":pwd_context.hash("1234") 
      }
}

# Hash_password
def hash_password(password:str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

# Create the Token
def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=30)
    to_encode.update({
        "exp":expire
    })
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

# LoginAPi /OAuth Form
@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends()):
    user = fake_user_db.get(form_data.username)
    if not user or not verify_password(form_data.password,user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid Username or password"
        )
    access_token = create_token({
        "sub":form_data.username
    })
    return {
        "access_token": access_token,
        "token_type": "bearer"
}

# Verify Token Function
def verify_token(token:str=Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )
        return username
    
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

# Protected Route
@app.get("/secure")
def secure(username:str = Depends(verify_token)):
    return{
        "Message":f"Hello!{username} Now you have acccessed the Secured data",
        "username":username
    }