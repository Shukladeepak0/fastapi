from fastapi import APIRouter 
from . import blog,user

mainrouter = APIRouter(
)

mainrouter.include_router(blog.router)
mainrouter.include_router(user.router)
