from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def hello():
    return "Hello from Service B!"

@app.get("/call-c")
def call_c():
    resp = requests.get("http://service-c:5002/")
    return f"Service B calling -> {resp.text}"