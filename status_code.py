from fastapi import FastAPI, status

app = FastAPI()

@app.post("/create",status_code=status.HTTP_201_CREATED)
def user_created():
    return{
        "Message":"User Created"
    }