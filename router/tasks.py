from fastapi import APIRouter, HTTPException
from mongo_db import MongoDB
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson import ObjectId
from models.Tasks import Task

tasks_router = APIRouter()
db = MongoDB()
collection = db.connect_collection(db_name="minerva-world", collection="tasks")

@tasks_router.get("/get-all")
def get_all():
    data = collection.find()
    tasks = [Task(**doc) for doc in data]
    json_data = jsonable_encoder(tasks)
    return JSONResponse(json_data)


@tasks_router.post("/create")
def create(task: Task):
    collection.insert_one(task.dict())
    return JSONResponse(task.dict())

@tasks_router.put("/update/{id}")
def update_task(id: str, task: Task):
    task_dict = task.dict()
    updated_task = collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": task_dict},
        return_document=True
    )
    if updated_task:
        return JSONResponse(task_dict)
    raise HTTPException(status_code=404, detail=f"Task {id} not found")
