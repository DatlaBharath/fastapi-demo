from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    valid_username = "admin"
    valid_password = "password123"
    if credentials.username != valid_username or credentials.password != valid_password:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/", dependencies=[Depends(authenticate)])
def hello():
    return "Hello from Service C!"