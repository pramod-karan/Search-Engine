
import requests
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import *
from model.api_schema import * 
from api_support.login_helper import *
from fastapi import APIRouter,HTTPException
from utils.connection import search_obj
from utils.connection import index_collection
from fastapi import status
from fastapi.responses import JSONResponse


helper_router = APIRouter(tags=["helper"])

# @helper_router.get("/create_index")
# async def create_index(token: str = Depends(oauth2_scheme)):

@helper_router.post('/create_index', response_model=Index)
def create_index(index : Index):
    "Creates an index for open search"

    index_body = {'settings': {'index': {'number_of_shards': 4}}}
    search_obj.indices.create(index.index_name, body=index_body)
    index_collection.insert_one({"index_name": index.index_name})
    response = {"success": True, "data": "", "message": "Index added Successfully"}
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)

@helper_router.get('/')
def check_service():
    ''' Checks if Open Search Engine is Healthy'''
    result =  requests.get('http://localhost:9200/').content
    return result

@helper_router.get('/health')
def check_health():
    ''' Checks if Open Search Engine is Healthy'''
    result =  requests.get('http://localhost:9200/_cluster/health').content
    return result
