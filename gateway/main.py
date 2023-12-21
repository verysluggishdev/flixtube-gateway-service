from fastapi import FastAPI
from .routers import users, auth, media, posts

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(media.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
