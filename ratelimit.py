from fastapi import FastAPI,Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse

app = FastAPI()

# Limiter Setup

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Error Handling
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request:Request,exc:RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail":"Too many requests"
        }
    )

@app.get("/data")
@limiter.limit("5/minutes")
def get_data(request:Request):
    return{
        "message":"Success"
    }