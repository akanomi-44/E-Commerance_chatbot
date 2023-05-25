from config import Config
import motor.motor_asyncio

class MongoDB:
    def __init__(self):
# pages
# clients
# templateReq
        self.host = Config.DB_CLUSTER
        self.userName = Config.DB_USER_NAME
        self.password = Config.DB_PASS
        self.database = 'Store'
        self.client = None
        self.db = None
        self.connect()
        
    def connect(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb+srv://{self.userName}:{self.password}@{self.host}/?retryWrites=true&compressors=zlib")
        self.db = self.client[self.database]

    def disconnect(self):
        if self.client:
            self.client.close()

    async def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        result = await collection.insert_one(document)
        return result.inserted_id

    async def find_documents(self, collection_name, query):
        collection = self.db[collection_name]
        cursor = collection.find(query)
        results = await cursor.to_list(length=None)
        return results

    async def find_one_document(self, collection_name, query):
        collection = self.db[collection_name]
        result = await collection.find_one(query)
        return result

    async def update_document(self, collection_name, query, update):
        collection = self.db[collection_name]
        result = await collection.update_one(query, update)
        return result.modified_count

    async def delete_document(self, collection_name, query):
        collection = self.db[collection_name]
        result = await collection.delete_one(query)
        return result.deleted_count
    
    async def find_one_and_update(self, collection_name, query, update, upsert):
        collection = self.db[collection_name]
        result = await collection.find_one_and_update(query, update, upsert=upsert)
        return result

db = MongoDB()
db.connect()