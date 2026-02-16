from fastapi import FastAPI
import requests
import redis

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

# New endpoint: Write data to Redis
@app.post("/redis-write/{key}/{value}")
def redis_write(key: str, value: str):
    r.set(key, value)
    return {"message": f"Stored {key} -> {value} in Redis"}

# New endpoint: Read data from Redis
@app.get("/redis-read/{key}")
def redis_read(key: str):
    value = r.get(key)
    if value:
        return {"key": key, "value": value}
    return {"message": f"{key} not found in Redis"}
