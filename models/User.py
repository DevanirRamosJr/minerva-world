from pydantic import BaseModel, StrictStr, StrictInt, Field
from typing import Optional

class User(BaseModel):
    username: StrictStr
    email: Optional[StrictStr] = Field(None)
    password: Optional[StrictStr] = Field(None)
    coins: StrictInt

class UserInDB(User):
    hashed_password: str