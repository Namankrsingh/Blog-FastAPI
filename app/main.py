from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import blog, users, comments
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(blog.router)
app.include_router(users.router)
app.include_router(comments.router)

app.mount("/media", StaticFiles(directory="media"), name="media")