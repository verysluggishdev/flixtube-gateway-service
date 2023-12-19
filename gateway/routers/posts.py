from typing import Optional
from .. import schemas,models, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db 
from sqlalchemy import func
from ..utils import generate_video_thumbnail, generate_unique_file_name
import os

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePostForm = Depends(), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    video_file_name = generate_unique_file_name(post.video.filename)
    
    try:
        
        if not os.path.exists('../uploads'):
            os.mkdir('../uploads')
        
        video_data = post.video.file.read()
        video_file_name = generate_unique_file_name(post.video.filename)
        
        try:
            extension = post.video.filename.split('.')[-1]
        except IndexError:
            extension = ""
        
        video_upload_path = f'../uploads/{video_file_name}.{extension}'
        
        with open(video_upload_path, 'wb') as f:
            f.write(video_data)
        
        thumbnail_file_name = generate_unique_file_name(f'thumbnail_{post.video.filename}.jpeg')
        
        thumbnail_upload_path = f'../uploads/{thumbnail_file_name}.jpeg'

        generate_video_thumbnail(video_upload_path, thumbnail_upload_path)


    except Exception as e:
        print(e)
        return {"message": "There was an error uploading the file"}
    
    finally:
        post.video.file.close()
    
    new_post = models.Post(title=post.title, 
                           description=post.description, 
                           thumbnail=thumbnail_file_name+".jpeg",
                           owner_id=current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)  
    
    return {"message": "post was successfully created"}
