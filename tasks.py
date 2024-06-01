from pydantic import BaseModel, StrictStr, StrictInt, StrictBool, Field
from typing import Optional

class Task(BaseModel):
    id: Optional[StrictStr] = Field(None, alias="_id")
    title: StrictStr
    description: StrictStr
    type: StrictStr
    is_completed: StrictBool
    value: StrictInt