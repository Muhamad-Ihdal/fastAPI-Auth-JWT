from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.post("/register")
def login()