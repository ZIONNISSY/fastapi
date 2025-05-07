from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

print(settings.database_hostname)

models.Base.metadata.create_all(bind=engine) # to create the tables in the database

app = FastAPI()

# origins = ["https://www.google.com"] # allowing access only to google.com

origins = ["*"]     # which means every domain/origins can access our app

# adding middleware so that the app can be accessed from different domains / origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router) # to include the post router in the main app
app.include_router(user.router) # to include the user router in the main app
app.include_router(auth.router) # to include the auth router in the main app
app.include_router(vote.router) # to include the vote router in the main app

@app.get("/")
def root():
    return {"message" : "Welcome to my api!!!"}