from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
import sqlalchemy
import os

router = APIRouter(
    prefix="/users",
    tags=['Users']
)




@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUserForm = Depends(), db: Session = Depends(get_db)):
    user.avatar = utils.handleFileUpload(user.avatar)
    
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    if db.query(models.User).filter(models.User.channelID == user.channelID).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"channelID is already in use")
    
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"email is already in use")

    new_user = models.User(**user.__dict__)
    db.add(new_user)
    db.commit()
    

    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user


@router.put("/{id}", response_model=schemas.UserResponse)
def update_user(id: int, user: schemas.UpdateUserForm = Depends(), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    user_query = db.query(models.User).filter(models.User.id==id)

    previous_user = user_query.first()
 
    if not previous_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
 
    if previous_user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update this user")


    if user.avatar:
        user.avatar = utils.handleFileUpload(user.avatar)
        os.remove(f'../uploads/{previous_user.avatar}')
    

    empty_attributes = [key for key, value in user.__dict__.items() if value is None]

    for attribute in empty_attributes:
        exec(f'del user.{attribute}')
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    user_query.update(user.__dict__, synchronize_session=False)
    db.commit()

    user = user_query.first().__dict__
    
    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id==id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete this user")
    os.remove(f'../uploads/{user.avatar}')
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)