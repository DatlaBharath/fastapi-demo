from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/")
def hello():
    return "Hello from Service B!"

@app.get("/call-c")
def call_c():
    url = "https://service-c:5002/"
    try:
        resp = requests.get(url, timeout=5)
        # Validate response status code
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to fetch data from Service C")
        # Validate content type
        if "application/json" not in resp.headers.get("Content-Type", ""):
            raise HTTPException(status_code=500, detail="Unexpected response format from Service C")
        return f"Service B calling -> {resp.text}"
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Service C: {str(e)}")