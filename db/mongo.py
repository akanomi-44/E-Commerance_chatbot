from pymongo import MongoClient
from config import Config

userName = Config.DB_USER_NAME
password = Config.DB_PASS
cluster = Config.DB_CLUSTER
uri = f"mongodb+srv://{userName}:{password}@{cluster}/?retryWrites=true&w=majority"  

client = MongoClient(uri)

db = client['Store']
pagesCollection = db['pages']
clientsCollection = db['clients']
templateReqCollection = db['templateReq']