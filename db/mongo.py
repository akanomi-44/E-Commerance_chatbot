from pymongo import MongoClient
from config import Config


host = Config.MONGODB_SETTINGS['host'] 
port = Config.MONGODB_SETTINGS['port']
db = Config.MONGODB_SETTINGS['db']
uri = f"mongodb://{host}:{port}/"  

client = MongoClient(uri)
