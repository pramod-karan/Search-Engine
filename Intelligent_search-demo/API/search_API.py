from tika import parser

import uuid
import time
import os
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
from datetime import datetime
from api_support.search_helper import load_dataset
from fastapi import status
from fastapi.responses import JSONResponse

search_router = APIRouter(tags=["search"])


# OAuth2 password bearer for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="search")

# @search_router.get("/create_index")
# async def create_index(token: str = Depends(oauth2_scheme)):

@search_router.post('/create_index', response_model=Index)
def create_index(index : Index):

    index_body = {
    'settings': {
        'index': {
        'number_of_shards': 4
        }
    }
    }
    response = search_obj.indices.create(
    index.index_name, 
    body=index_body)

    return response

# @search_router.get("/load_data",response_model=Data)
# async def load_data(token: str = Depends(oauth2_scheme), data : Data):
@search_router.post('/load_data',response_model=Data)
def load_data(data : Data):

    file_path = data.source_path
    print("file_path ====================== : ", file_path)
    file_list = load_dataset(file_path)

    response = {"success": True, "data": "", "message": "Added {} file".format(len(file_list))}
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


# @search_router.get("/search")
# async def search(token: str = Depends(oauth2_scheme)):
@search_router.get('/search')
async def search(request: Request):

    payload = request.query_params
    query = payload["query"]
    exact = payload["exact"]
    start_time = time.time()

    print("exact :", exact)
    if exact == "true":
        print("here")
        payload = {
            # "_source": {"excludes": [ "parsed_content" ]},
            'query': {'match_phrase': {'parsed_content': query}}
                    }
    else:
        print("there")
        payload = {
            # "_source": {"excludes": [ "parsed_content" ]},
            'query': {'match': {'parsed_content': query}}
                    }
    


    result = search_obj.search(
        body=payload,
        index=INDEX_NAME
    )
    
    # response = {"time_taken": result["took"],
	# "total_items" : result["hits"]["total"],
	# "max_score":result["hits"]["max_score"],
	# "results":result["hits"]["hits"]
    # }
    response = { "results":result["hits"]["hits"]}
	
    print("Time Taken--- %s seconds ---" % (time.time() - start_time))
    return response


#additional functionalities
    

# @search_router.get("/pdf_count")
# async def pdf_count(token: str = Depends(oauth2_scheme)):
@search_router.get('/pdf_count')
def pdf_count():
    ''' Get number of pdf in an index'''
    result =  requests.get('http://localhost:9200/_cat/count/pdf_search?v').content
    return result

@search_router.get('/get_pdf')
def get_pdf():
    ''' Get pdf data'''
    pdf_id = request.args.get('id')
    result =  requests.get('http://localhost:9200/pdf_search/_doc/{}'.format(pdf_id)).content
    return result

@search_router.post('/delete_index')
def delete_index():
    ''' Delete Index'''
    print("Deleting Records")
    search_obj.indices.delete(index=INDEX_NAME)
    return "Deleted all records"