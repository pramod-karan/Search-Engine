from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import *
from fastapi import APIRouter,HTTPException
from opensearchpy import OpenSearch

# MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]
users_collection = db["users"]
index_collection = db["index"]

#opensearch client
search_obj = OpenSearch("http://localhost:9200/", timeout = 6000)

#es = Elasticsearch(timeout=30, max_retries=10, retry_on_timeout=True)



# net start MongoDB