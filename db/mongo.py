from pymongo import MongoClient
from config import Config


host = Config.MONGODB_SETTINGS['host'] 
port = Config.MONGODB_SETTINGS['port']

userName = Config.DB_USER_NAME
password = Config.DB_PASS
cluster = Config.DB_CLUSTER
uri = f"mongodb://{userName}:{password}@{cluster}/?retryWrites=true&w=majority"  

client = MongoClient(uri)

db = client['Store']
pagesCollection = db['pages']
