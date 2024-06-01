from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decouple import config

uri = f"mongodb+srv://minerva:{config('DB_PASSWORD')}@minerva.cjz3gqd.mongodb.net/?retryWrites=true&w=majority&appName=Minerva"


class MongoDB:
    def __init__(self):
        self.client = None
        self.connect()

    def connect(self):
        self.client = MongoClient(uri, server_api=ServerApi('1'))

        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def connect_collection(self, db_name, collection):
        db = self.client.get_database(db_name)
        collection = db.get_collection(collection)
        return collection
        # c = b.find({"title":"Title Goes Here"})
        # print(a.tasks.find_one({"title":"Title Goes Here"}))
        # for task in b.find():
        #     print(task)

def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "type": task["type"],
        "is_completed": task["is_completed"],
        "value": task["value"],
    }