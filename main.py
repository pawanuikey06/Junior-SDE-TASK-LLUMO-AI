from fastapi import FastAPI
from database import db
from routes import employees



app = FastAPI(title="Employee API", version="1.0")


# Including Routers
app.include_router(employees.router)

@app.get("/")
async def home():
    collections = await db.list_collection_names()
    return {
        "message": "FastAPI + MongoDB (Motor) setup successful!",
        "collections": collections
    }