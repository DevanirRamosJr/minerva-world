from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.tasks import tasks_router

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title="Minerva World"
)

origins = [
    "http://localhost:8081",
    "https://665cf5452a91430e81a24bc7--minerva-world.netlify.app",
    "https://main--minerva-world.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(tasks_router, prefix="/task")

