from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from .. import oauth2
import os


router = APIRouter(
    prefix="/media",
    tags=["Media"]
)

@router.get("/{filename}")
def get_post(filename: str):
    if not os.path.exists(f'../uploads/{filename}'):
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return FileResponse(f'../uploads/{filename}', filename=filename)



