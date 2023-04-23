from pymongo import MongoClient


uri = ""

client = MongoClient(uri)
db = client['mydatabase']
