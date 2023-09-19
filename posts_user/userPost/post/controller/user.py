from sqlalchemy.orm import session
from ..Models import models
from ..Schemas import schemas
from fastapi import status, HTTPException, File, UploadFile
from passlib.context import CryptContext
import uuid
import os
import magic 

IMAGEDIR = "post/images/"
MAX_FILE_SIZE = 2*1024*1024
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_image_mime_type(file_path):
    mime = magic.Magic()
    mime_type = mime.from_file(file_path)
    return mime_type

def create(request: schemas.User,db: session):
    try:
        hashedPassword = pwd_cxt.hash(request.password)
        new_user = models.User(firstname = request.firstname,lastname = request.lastname,email = request.email,mobile = request.mobile, gender = request.gender, password = hashedPassword, status = request.status, profilepic = "null")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=422, detail="An User has been already registerd with this email, Please try with another one.")

def show(id: int, db: session):
    User = db.query(models.User).filter(models.User.id == id).first()
    if not User:
        raise HTTPException(status_code=400,detail=f"User with the id {id} is  not available.")
    return User

def all(db: session):
    users = db.query(models.User).all()
    return users

def update(id: int, request: schemas.User, db: session):
    # Check if the provided 'id' exists, and if not, raise an HTTPException
    existing_user = db.query(models.User).filter(models.User.id == id).first()
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id : {id} not found")

    hashedPassword = pwd_cxt.hash(request.password)
    # Update the post with the new data
    existing_user.firstname = request.firstname
    existing_user.lastname = request.lastname
    existing_user.email = request.email
    existing_user.mobile = request.mobile
    existing_user.gender = request.gender
    existing_user.status = request.status
    existing_user.password = hashedPassword

    db.commit()
    db.refresh(existing_user)
    return existing_user

def destroy(id: int, db: session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id : {id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return "Deleted"


def toggle(user_id,db: session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    current_status = user.status
    if current_status == "inactive":
        new_status = "active" 
    elif current_status == "active":
        new_status = "inactive"
    
    user.status = new_status
    db.commit()
    return {"message": f"User status toggled to {new_status}"}

async def profilepic(user_id: int,file: UploadFile,db:session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id : {user_id} not found")
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    with open(f"{IMAGEDIR}{file.filename}","wb") as f:
        f.write(contents)
    mime_type = get_image_mime_type(f"{IMAGEDIR}{file.filename}")
    mime_type = mime_type.lower()
    if not ("png" in mime_type or "jpg" in mime_type or "jpeg" in mime_type):
        if os.path.exists(f"{IMAGEDIR}{file.filename}"):
            os.remove(f"{IMAGEDIR}{file.filename}") 
        return ["please enter valid image we allow only (png, jpg, and jpeg)"]
    elif os.path.getsize(f"{IMAGEDIR}{file.filename}") > MAX_FILE_SIZE:
        if os.path.exists(f"{IMAGEDIR}{file.filename}"):
            os.remove(f"{IMAGEDIR}{file.filename}") 
        return ["Image size should be not more than 2mb"]
    else:
        user.profilepic = file.filename
        db.commit()
        db.refresh(user)
        return user