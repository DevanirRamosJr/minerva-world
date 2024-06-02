from fastapi import APIRouter, HTTPException
from mongo_db import MongoDB, task_helper
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson import ObjectId
from typing import Dict

tasks_router = APIRouter()
db = MongoDB()
collection = db.connect_collection(db_name="minerva-world", collection="tasks")

@tasks_router.get("/get-all")
def get_all():
    data = collection.find()
    tasks = [task_helper(task) for task in data]
    json_data = jsonable_encoder(tasks)
    return JSONResponse(json_data)


@tasks_router.post("/create")
def create(task: Dict):
    print(task)
    task["_id"] = ObjectId()
    collection.insert_one(task)
    return task_helper(task)

@tasks_router.put("/update/{id}")
def update_task(id: str, task):
    task_dict = task.dict()
    updated_task = collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": task_dict},
        return_document=True
    )
    if updated_task:
        return task_helper(updated_task)
    raise HTTPException(status_code=404, detail=f"Task {id} not found")
