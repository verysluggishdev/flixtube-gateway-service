from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy import func
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
def get_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    subscriber_count = db.query(func.count(models.Subscribers.subscribed_to)).filter(models.Subscribers.subscribed_to == id).scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    
    is_subscribed = db.query(models.Subscribers).filter(models.Subscribers.subscribed_to == id).filter(models.Subscribers.user_id == current_user.id).first() != None

    return {**user.__dict__, 'subscriber_count':subscriber_count, 'subscribed': is_subscribed}


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
        try:
            os.remove(f'../uploads/{previous_user.avatar}')
        except Exception as e:
            print(e)
    

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
    try:
        os.remove(f'../uploads/{user.avatar}')
    except Exception as e:
        print(e)
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def subscribe_to_user(id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id==id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")    
    current_subscription_query = db.query(models.Subscribers).filter(models.Subscribers.user_id == current_user.id).filter(models.Subscribers.subscribed_to == id)
    has_subscribed = current_subscription_query.first()
    if has_subscribed:
        current_subscription_query.delete(synchronize_session=False)
    else:
        new_subscription = models.Subscribers(user_id=current_user.id, subscribed_to=id)
        db.add(new_subscription)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)