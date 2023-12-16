from typing import Optional
from .. import schemas,models, oauth2
from fastapi import Depends, APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db 


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("")
def upload(file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    new_avatar = models.Avatar(owner_id=current_user.id, filename=file.filename)
    db.add(new_avatar)
    db.commit()
    db.refresh(new_avatar)

    return {"message": f"Successfully uploaded {file.filename}"}