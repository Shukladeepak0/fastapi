from sqlalchemy.orm import session
from ..Models import models
from ..Schemas import schemas
from fastapi import status, HTTPException

def get_all(db: session):
    blogs = db.query(models.Post).all()
    return blogs

def create(request: schemas.Post,db: session):
    User = db.query(models.User).filter(models.User.id == request.User_id).first()
    if not User:
        getUser = db.query(models.User).filter(models.User.status == "active").all()
        return {"detail": f"User with the id {request.User_id} is  not available.", "Active Users": getUser}
    new_post = models.Post(tittle=request.tittle, body=request.body, user_id=request.User_id, status= request.status)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    return new_post

def destroy(id: int,db: session):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return "Deleted"

def update(id: int,request: schemas.Post, db: session):
    # Check if the provided 'id' exists, and if not, raise an HTTPException
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} not found")

    # Update the post with the new data
    existing_post.tittle = request.tittle
    existing_post.body = request.body

    db.commit()
    db.refresh(existing_post)
    return existing_post

def show(id: int, db: session):
    blog = db.query(models.Post).filter(models.Post.id == id).first()
    if not blog:
        raise HTTPException(status_code=400,detail=f"Post with the id {id} is  not available.")
    return blog

def search(query_param, db: session):
    if query_param.isdigit():
        user_id = int(query_param)
        posts = db.query(models.Post).filter(models.Post.user_id == query_param).all()
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found with the given Id")
        return posts
    else:
        posts = db.query(models.Post).filter(models.Post.tittle.ilike(f"%{query_param}%")).all()
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found with the given title")
        return posts
    