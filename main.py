from fastapi import FastAPI
from routes import employees
from database import db

app = FastAPI(title="Employee API", version="1.0")
app.include_router(employees.router)

@app.get("/")
async def home():
    collections = await db.list_collection_names()
    return {
        "message": "FastAPI + MongoDB (Motor) setup successful!",
        "collections": collections
    }
