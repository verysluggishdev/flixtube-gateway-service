from fastapi import Depends, APIRouter
from fastapi.responses import FileResponse
from .. import oauth2


router = APIRouter(
    prefix="/media",
    tags=["Media"]
)

@router.get("/{filename}")
def get_post(filename: str, current_user: int = Depends(oauth2.get_current_user)):
    return FileResponse(f'../uploads/{filename}', filename=filename)



