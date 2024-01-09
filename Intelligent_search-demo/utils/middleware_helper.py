
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import *
from fastapi import APIRouter,HTTPException


async def check_logged_user(request: Request, call_next):
    """
    Middleware to check if the user is already logged in based on the access token.

    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable): The next callable in the middleware chain.

    Raises:
        HTTPException: Raised if the user is already logged in.

    Returns:
        Response: The HTTP response.
    """
    print("Code Reached Middleware")
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    print("token : ", token)
    username = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        pass
    
    print("logged_in_users :", logged_in_users)
    if username and username in logged_in_users:
        raise HTTPException(status_code=400, detail="User is already logged in")
    
    response = await call_next(request)
    return response