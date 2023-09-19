from fastapi import APIRouter, Query
from typing import List
from fastapi import Depends, status, Response
from ..Schemas import schemas
from ..Database.database import get_db
from sqlalchemy.orm import Session
from ..controller import blog

router = APIRouter(
    tags=["Posts"]
)

@router.get("/posts",status_code=status.HTTP_200_OK,response_model=List[schemas.showPost])
def all(db: Session = Depends(get_db)):
    return blog.get_all(db)

@router.get("/post/{id}",status_code=status.HTTP_200_OK, response_model=schemas.showPost)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    return blog.show(id,db)

@router.post("/post", status_code= status.HTTP_201_CREATED)
def create(request: schemas.Post, db: Session = Depends(get_db)):
    return blog.create(request,db)

@router.put("/post/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Post, db: Session = Depends(get_db)):
    return blog.update(id,request,db)

@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db : Session = Depends(get_db)):
    return blog.destroy(id,db)


@router.get("/posts/by_title/")
def search_posts_by_title(query_param: str = Query(..., description="Search by user ID or post title"), db: Session = Depends(get_db)):
   return blog.search(query_param,db)