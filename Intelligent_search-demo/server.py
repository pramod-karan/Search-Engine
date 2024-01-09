import uvicorn
from fastapi import FastAPI
from API import login_API, search_API, support_API
from utils.middleware_helper import check_logged_user

from fastapi import FastAPI, Depends, HTTPException, Request

app = FastAPI()
app.include_router(login_API.security)
app.include_router(search_API.search_router)
app.include_router(support_API.helper_router)


@app.middleware("http")
def check_logged_in_user(request: Request, call_next):
    """ Middleware to check if the user is already 
    logged in based on the access token."""
    return check_logged_user(request, call_next)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=5000, reload=True)

