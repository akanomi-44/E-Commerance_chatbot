from pymongo import MongoClient
from config import Config


host = Config.MONGODB_SETTINGS['host'] 
port = Config.MONGODB_SETTINGS['port']
db = Config.MONGODB_SETTINGS['db']
uri = f"mongodb+srv://hiiamhoan:pKl2fFmfQUDzUuL7@cluster0.spa4890.mongodb.net/?retryWrites=true&w=majority"  

client = MongoClient(uri)
