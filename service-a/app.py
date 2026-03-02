from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
import requests
import redis
import re

app = FastAPI()

# Connect to Redis service in Minikube
r = redis.Redis(host="redis-service", port=6379, decode_responses=True)

@app.get("/")
def hello():
    return "Hello from Service A!"

@app.get("/call-b")
def call_b():
    resp = requests.get("http://service-b:5001/")
    return f"Service A calling -> {resp.text}"

@app.get("/call-c-a")
def call_c_a():
    resp = requests.get("http://service-c:5002/")
    return f"Service A calling -> {resp.text}"

# Input validation model for Redis write
class RedisWriteInput(BaseModel):
    key: constr(regex=r"^[a-zA-Z0-9_-]+$", max_length=256)  # Alphanumeric, underscores, hyphens, max length 256
    value: constr(max_length=1024)  # Max length 1024

# New endpoint: Write data to Redis
@app.post("/redis-write/")
def redis_write(input_data: RedisWriteInput):
    sanitized_key = re.sub(r"[^\w-]", "", input_data.key)  # Remove unwanted characters
    sanitized_value = re.sub(r"[^\w\s-]", "", input_data.value)  # Remove unwanted characters
    r.set(sanitized_key, sanitized_value)
    return {"message": f"Stored {sanitized_key} -> {sanitized_value} in Redis"}

# New endpoint: Read data from Redis
@app.get("/redis-read/{key}")
def redis_read(key: str):
    if not re.match(r"^[a-zA-Z0-9_-]+$", key):  # Validate key format
        raise HTTPException(status_code=400, detail="Invalid key format")
    value = r.get(key)
    if value:
        return {"key": key, "value": value}
    return {"message": f"{key} not found in Redis"}