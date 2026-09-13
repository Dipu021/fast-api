from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def log_middleware(request:Request,call_next):
    start_time = time.time()
    response = await call_next(request)
    processed_time = time.time()-start_time
    print(f"Path:{request.url.path}|Time:{processed_time}")
    return response