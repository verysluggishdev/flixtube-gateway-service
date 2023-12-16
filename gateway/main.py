from fastapi import FastAPI
from .routers import users, auth, upload

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(upload.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
