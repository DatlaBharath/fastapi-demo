from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
import requests
import redis
import re
import ssl

app = FastAPI()

# Configure Redis connection with TLS
ssl_context = ssl.create_default_context(cafile="/path/to/ca-cert.pem")
ssl_context.load_cert_chain(certfile="/path/to/client-cert.pem", keyfile="/path/to/client-key.pem")
r = redis.Redis(host="redis-service", port=6379, ssl=True, ssl_context=ssl_context, decode_responses=True)

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