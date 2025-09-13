from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# loading env variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Connecting With MONGO-DB (async)
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
employee_collection = db[COLLECTION_NAME]