import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    valid_username = os.getenv("VALID_USERNAME")
    valid_password = os.getenv("VALID_PASSWORD")
    if not valid_username or not valid_password:
        raise HTTPException(status_code=500, detail="Server misconfiguration: Missing credentials")
    if credentials.username != valid_username or credentials.password != valid_password:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/", dependencies=[Depends(authenticate)])
def hello():
    return "Hello from Service C!"