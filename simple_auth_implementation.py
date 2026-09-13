from fastapi import FastAPI, Depends,Header,HTTPException

app = FastAPI()

def verify_token(token:str=Header(None)):
     if token != "mysecrettoken":
          raise HTTPException(
               status_code=401,
               detail="UnAuthorozed"
          )
     return{
          "User":"Authorozed User"
     }

@app.get("/secure_data")
def secure_data(user = Depends(verify_token)):
     return{
          "Message":"Secure data accessed",
          "System":user
     }