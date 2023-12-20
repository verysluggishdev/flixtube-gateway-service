from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
import sqlalchemy

router = APIRouter(
    prefix="/users",
    tags=['Users']
)




@router.post("", status_code=status.HTTP_201_CREATED)
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


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user