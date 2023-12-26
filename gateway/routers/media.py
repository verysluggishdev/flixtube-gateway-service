from fastapi import Depends, APIRouter
from fastapi.responses import FileResponse
from .. import oauth2


router = APIRouter(
    prefix="/media",
    tags=["Media"]
)

@router.get("/{filename}")
def get_post(filename: str):
    return FileResponse(f'../uploads/{filename}', filename=filename)



