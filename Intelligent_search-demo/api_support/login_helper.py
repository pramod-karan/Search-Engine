from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import *
from fastapi import APIRouter,HTTPException
from utils.connection import users_collection

# Create a function to get a user from the database
def get_user(username: str):
    """
    Retrieve user data from the MongoDB database.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        dict: User data if found, None if not found.
    """
    user = users_collection.find_one({"username": username})
    return user

def get_email(email: str):
    """
    Retrieve user data from the MongoDB database.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        dict: User data if found, None if not found.
    """
    user = users_collection.find_one({"email": email})
    return user


# Create a function to generate an access token
def create_access_token(data: dict, expires_delta: timedelta = 15):
    """
    Generate a JWT access token.

    Args:
        data (dict): Data to encode in the token.
        expires_delta (timedelta, optional): Token expiration time. Defaults to None.

    Returns:
        str: Generated JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Password hashing
class Hasher:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str):
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)