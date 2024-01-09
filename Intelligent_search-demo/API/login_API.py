from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from utils.config import *
from model.api_schema import * 
from api_support.login_helper import *
from fastapi import APIRouter,HTTPException
from utils.connection import users_collection
import json
from fastapi import status
from fastapi.responses import JSONResponse

security = APIRouter(tags=["login"])


hasher = Hasher()

# OAuth2 password bearer for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@security.post("/register", response_model=User)
async def register(user: User):
    """
    Register a new user.

    Args:
        user (User): User data including username, password and email.

    Returns:
        User: Registered user data.
    """
    existing_user = await get_user(user.username)
    existing_email = await get_email(user.email)

    if existing_user or existing_email:
        raise HTTPException(status_code=400, detail={"success": False, "data": "", "message": "Username/Email already registered"})
    
    hashed_password = hasher.hash_password(user.password)
    inserted_id  = users_collection.insert_one({"username": user.username, "password": hashed_password,"email": user.email}).inserted_id
    
    response = {"success": True, "data": str(inserted_id), "message": "User resgistered successfully"}
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    


@security.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get an access token for authentication.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data including username and password.

    Returns:
        dict: Token response including access token and token type.
    """
    user_data = await get_user(form_data.username)

    if user_data["username"] in logged_in_users.keys():
        response = {"success": False, "data": "", "message": "User already Logged In"}
        return JSONResponse(content=response, status_code=status.HTTP_406_NOT_ACCEPTABLE)
    
    if not user_data or not hasher.verify_password(form_data.password, user_data["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data["username"]}, expires_delta=access_token_expires)
    
    logged_in_users[user_data["username"]] = access_token
    
    response = {"success": True, "data": access_token, "message": "Logged In Successfully"}
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@security.post("/logout")
async def logout(request: Request):
    """
    Log out the user and remove them from the logged-in users dictionary.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        dict: Response message.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    username = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        pass
    if username and username in logged_in_users:
        del logged_in_users[username]
        
    response = {"success": True, "data": "", "message": "Logged out successfully"}
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@security.get("/protected-route")
async def protected_route(token: str = Depends(oauth2_scheme)):
    """
    A protected route that requires authentication.

    Args:
        token (str): JWT access token.

    Returns:
        dict: Response message.
    """
    user = await get_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "This is a protected route"}