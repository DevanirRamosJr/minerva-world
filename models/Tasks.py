from typing import Optional
from pydantic import BaseModel, StrictStr, StrictInt, StrictBool, Field
from models.PyObjectId import PyObjectId


class Task(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    title: StrictStr
    description: StrictStr
    type: StrictStr
    is_completed: StrictBool
    value: StrictInt
    created: Optional[StrictInt] = Field(None)

    class Config:
        json_encoders = {
            PyObjectId: lambda v: str(v),
        }


