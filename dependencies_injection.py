from fastapi import FastAPI , Depends

app = FastAPI()

def get_current_user():
    return{
        "User":"John"
    }

@app.get("/profile")
def profile(user =Depends(get_current_user)):
    return user


@app.get("/dasjboard")
def profile(user =Depends(get_current_user)):
    return user