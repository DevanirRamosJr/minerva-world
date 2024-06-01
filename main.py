from fastapi import FastAPI
from mongo_db import MongoDB, task_helper
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from router.tasks import tasks_router

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title="Minerva World"
)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(tasks_router, prefix="/task")

