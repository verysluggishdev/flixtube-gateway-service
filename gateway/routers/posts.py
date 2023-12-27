from typing import Optional
from .. import schemas,models, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db 
from sqlalchemy import func
from ..utils import handleFileUpload, generate_unique_file_name, generate_video_thumbnail
from sqlalchemy.orm import joinedload
import os

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePostForm = Depends(), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    video_file_name = handleFileUpload(post.video)

    thumbnail_file_name = generate_unique_file_name(f"thumbnail_{post.video}")+'.jpeg'

    generate_video_thumbnail(f'../uploads/{video_file_name}', f'../uploads/{thumbnail_file_name}')
    
    new_post = models.Post(title=post.title, 
                           description=post.description, 
                           thumbnail=thumbnail_file_name,
                           video=video_file_name,
                           owner_id=current_user.id,
                           category=post.category
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)  
    
    return {"message": "post was successfully created"}

@router.put("/{id}")
def update_post(id: int, post: schemas.UpdatePostForm = Depends(), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id==id)

    previous_post = post_query.first()
 
    if not previous_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
 
    if previous_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update this post")

    if post.video:
        os.remove(f'../uploads/{previous_post.thumbnail}')
        os.remove(f'../uploads/{previous_post.video}')
        post.video = handleFileUpload(post.video)
        thumbnail_file_name = generate_unique_file_name(f"thumbnail_{post.video}")+'.jpeg'
        generate_video_thumbnail(f'../uploads/{post.video}', f'../uploads/{thumbnail_file_name}')
        post.thumbnail = thumbnail_file_name


    empty_attributes = [key for key, value in post.__dict__.items() if value is None]

    for attribute in empty_attributes:
        exec(f'del post.{attribute}')
    
    post_query.update(post.__dict__, synchronize_session=False)
    db.commit()
            
    return {"message": "post was successfully updated"}


@router.get("/{id}", response_model=schemas.SinglePostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = (
        db.query(models.Post)
        .join(models.User, models.User.id == models.Post.owner_id)
        .filter(models.Post.id == id)  
        .options(joinedload(models.Post.owner))
        .first()
    )

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")


    likes_count = db.query(func.count()).filter(models.PostMetrics.liked.is_(True)).scalar()
    dislikes_count = db.query(func.count()).filter(models.PostMetrics.disliked.is_(True)).scalar()
    shares_count = db.query(func.count()).filter(models.PostMetrics.shared.is_(True)).scalar()


    post_metrics = {
        'likes': likes_count,
        'dislikes': dislikes_count,
        'shares': shares_count
    }

    response = {**post.__dict__, **post_metrics}

    return response

@router.get("", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), category: str = 'all', limit: int = 10, skip: int = 0, search: Optional[str]=""):

    items = (
    db.query(models.Post)
    .join(models.User, models.User.id == models.Post.owner_id)
    )

    if category != 'all':
        items = items.filter(models.Post.category == category)
    
    items = items.options(joinedload(models.Post.owner)).filter(models.Post.title.contains(search) | models.Post.description.contains(search)).limit(limit).offset(skip).all()

    return items


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete this post")
    os.remove(f'../uploads/{post.thumbnail}')
    os.remove(f'../uploads/{post.video}')
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)