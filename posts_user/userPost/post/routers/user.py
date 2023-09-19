from typing import List
from fastapi import APIRouter 
from fastapi import Depends, status, Response, File, UploadFile
from ..Schemas import schemas
from ..Database.database import get_db
from sqlalchemy.orm import Session
from ..controller import user

router = APIRouter(
    tags=["Users"]
)

@router.post("/user",response_model=schemas.showUser)
async def create_user(request: schemas.User, db : Session = Depends(get_db)):
    return user.create(request,db)

@router.get("/user/{id}",status_code=status.HTTP_200_OK, response_model=schemas.showUser)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    return user.show(id,db)

@router.get("/users",status_code=status.HTTP_200_OK,response_model=List[schemas.showUser])
def all(db: Session = Depends(get_db)):
    return user.all(db)

@router.put("/user/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.User, db: Session = Depends(get_db)):
    return user.update(id, request, db)

@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db : Session = Depends(get_db)):
    return user.destroy(id, db)

@router.put("/profilepic/{user_id}")
async def profilepic(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await user.profilepic(user_id,file,db)


@router.put("/toggle-status/{user_id}")
async def toggle_user_status(user_id: int, db: Session = Depends(get_db)):
    return user.toggle(user_id,db)


