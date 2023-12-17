from .. import models, oauth2
from fastapi import Depends, APIRouter, UploadFile, File, status
from sqlalchemy.orm import Session
from ..database import get_db 
from ..utils import generate_unique_file_name
import os



router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def upload(file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    current_avatar = db.query(models.Avatar).filter(models.Avatar.owner_id == current_user.id).first()

    try:
        
        if not os.path.exists('../uploads'):
            os.mkdir('../uploads')
        
        contents = file.file.read()
        filename = generate_unique_file_name(file.filename)
        
        try:
            extension = file.filename.split('.')[1]
        except IndexError:
            extension = ""
        
        with open(f'../uploads/{filename}.{extension}', 'wb') as f:
            f.write(contents)

    except Exception as e:
        print(e)
        return {"message": "There was an error uploading the file"}
    
    finally:
        file.file.close()

    if current_avatar:
        os.remove(f'../uploads/{current_avatar.filename}')
        current_avatar.filename = f'{filename}.{extension}'
        db.commit()
        return {"message": f"Avatar was updated successfully"}
        
    new_avatar = models.Avatar(owner_id=current_user.id, filename=f'{filename}.{extension}')
    db.add(new_avatar)
    db.commit()
    return {"message": f"Avatar was created successfully"}