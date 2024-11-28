from fastapi import FastAPI, Depends, HTTPException

from taskapp.routers import auth, posts

app = FastAPI()

app.include_router(auth.router)
app.include_router(posts.router)