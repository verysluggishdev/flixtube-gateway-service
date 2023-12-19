from typing import Optional
from .. import schemas,models, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db 
from sqlalchemy import func
from ..utils import  handleVideoUpload
import os

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePostForm = Depends(), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    video_file_name, thumbnail_file_name = handleVideoUpload(post.video)
    
    new_post = models.Post(title=post.title, 
                           description=post.description, 
                           thumbnail=thumbnail_file_name,
                           video=video_file_name,
                           owner_id=current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)  
    
    return {"message": "post was successfully created"}

@router.put("/{id}")
def create_post(id: int, post: schemas.UpdatePostForm = Depends(), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id==id)

    previous_post = post_query.first()
 
    if not previous_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
 
    if previous_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update this post")

    empty_attributes = [key for key, value in post.__dict__.items() if value is None]

    for attribute in empty_attributes:
        exec(f'del post.{attribute}')

    fields = dict()

    if post.video.filename:

        os.remove(f'../uploads/{previous_post.thumbnail}')
        os.remove(f'../uploads/{previous_post.video}')
        data = handleVideoUpload(post.video)
        video_file_name, thumbnail_file_name = data
        fields.update({'thumbnail': thumbnail_file_name, 'video': video_file_name})


    del post.video

    fields.update(post.__dict__)

    post_query.update(fields, synchronize_session=False)
    db.commit()
            
    return {"message": "post was successfully updated"}


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete this post")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)