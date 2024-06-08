from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.tasks import tasks_router
from router.users import users_router
from mongo_db import MongoDB

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title="Minerva World"
)

origins = [
    "http://localhost:8081",
    "https://minerva-world.netlify.app",
    "https://main--minerva-world.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router, prefix="/task")
app.include_router(users_router, prefix="/user")
