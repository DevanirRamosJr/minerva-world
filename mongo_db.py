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
