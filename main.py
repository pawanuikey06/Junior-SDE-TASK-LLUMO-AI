from fastapi import FastAPI
from database import db

app = FastAPI(title="Employee API", version="1.0")

@app.get("/")
async def home():
    collections = await db.list_collection_names()
    return {
        "message": "FastAPI + MongoDB (Motor) setup successful!",
        "collections": collections
    }