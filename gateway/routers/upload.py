from typing import Optional
from .. import schemas,models, oauth2
from fastapi import Depends, APIRouter, UploadFile, File, status
from sqlalchemy.orm import Session
from ..database import get_db 
from ..utils import generate_unique_file_name
import os
import base64


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def upload(file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    try:
        if not os.path.exists('../../uploads'):
            os.mkdir('../../uploads')
        contents = file.file.read()
        filename = generate_unique_file_name(file.filename)
        print(base64.b64decode(filename.encode()))
        with open(f'uploads/{filename}', 'wb') as f:
            f.write(contents)
    except Exception as e:
        print(e)
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    new_avatar = models.Avatar(owner_id=current_user.id, filename=filename)
    db.add(new_avatar)
    db.commit()
    db.refresh(new_avatar)
    return {"message": f"Avatar was updated successfully"}