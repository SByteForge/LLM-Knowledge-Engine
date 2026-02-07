from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time
import uuid
import ollama

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str

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

@app.post("/generate/")
def generate(request: GenerateRequest):
    start_time = time.time()
    
    response = ollama.chat(
        model="mistral:latest",
        messages=[{"role": "user", "content": request.prompt}]
    )
    
    return {
        "request_id": str(uuid.uuid4()),
        "prompt": request.prompt,
        "response": response["message"]["content"],
        "latency_ms": round((time.time() - start_time) * 1000, 2)
    }
    
    
def stream_llm_response(prompt: str):
    stream = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in stream:
        yield chunk["message"]["content"]
    
    
@app.post("/generate-stream/")
def generate_stream(request: GenerateRequest):
    return StreamingResponse(
        stream_llm_response(request.prompt),
        media_type="text/plain"
        )
