from bson.errors import InvalidId
from bson import ObjectId as BaseObjectId

class PyObjectId(str):
    @classmethod
    def validate(cls, value, alias):
        """Validate given str value to check if good for being ObjectId."""
        try:
            return BaseObjectId(str(value))
        except InvalidId as e:
            raise ValueError("Not a valid ObjectId") from e

    @classmethod
    def __get_validators__(cls):
        yield cls.validate