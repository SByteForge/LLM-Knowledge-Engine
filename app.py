from fastapi import FastAPI
import time
import uuid

app = FastAPI()

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message" : "API is running"
        }


@app.get("/ping")
def ping():
    start_time = time.time()
    response = {
        "request_id": str(uuid.uuid4()),
        "message": "pong!",
        "latency_ms": round((time.time() - start_time) * 1000, 2)
    }
    return response


@app.get("/hello")
def hello():
    return {
        "message": "Hello, World!"
    }