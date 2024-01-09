from pydantic import BaseModel

# Define a Pydantic model for user input data
class User(BaseModel):
    username: str
    password: str
    email:str

class Search(BaseModel):
    query: str

class Data(BaseModel):
    source_path: str

class Index(BaseModel):
    index_name: str