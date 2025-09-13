from fastapi import FastAPI
from routes import employees,analytics
from database import db

app = FastAPI(title="Employee API", version="1.0")
app.include_router(employees.router, prefix="/employees")

app.include_router(analytics.router, prefix="/analytics")

@app.get("/")
async def home():
    collections = await db.list_collection_names()
    return {
        "message": "FastAPI + MongoDB (Motor) setup successful!",
        "collections": collections
    }
