import pymongo
import pandas as pd
import openai
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity
from config import Config

openai.api_key = Config.OPENAI_API_KEY

class Server:
    def __init__(self,dbName, collectionName, clientName= "mongodb://localhost:27017/", embField = "req" ):
        self.client = pymongo.MongoClient(clientName)
        self.db = self.client[dbName]
        self.collection = self.db[collectionName]
        self.embField = embField
    
    def addData(self,data: list):
        self.collection.insert_many(data)
    
    def printData(self):
        for item in self.collection.find():
            print(item)

    def toDF(self):
        df = pd.DataFrame(list(self.collection.find()))
        return df

    def embeddingData(self,field):
        '''Add embeded value of req'''
        if self.embField != field:
            self.embField = field
            
        df = pd.DataFrame(list(self.collection.find()))
        df['embedding'] = df[field].apply(lambda x: get_embedding(x , engine='text-embedding-ada-002'))
        
        for doc in self.collection.find():
            embedding = df.loc[df['_id'] == doc['_id'], 'embedding'].values[0]
            
            self.collection.update_one({'_id': doc['_id']}, {'$set': {'embedding': embedding}})

    def dropCollection(self, dbName=None,collectionName=None):
        if dbName is None or collectionName is None:
            dbName = self.db.name
            collectionName = self.collection.name
            
        if dbName in self.client.list_database_names():
            db = self.client[dbName]
            if collectionName in db.list_collection_names():
                db[collectionName].drop()
                print(f"Collection {collectionName} dropped successfully from {dbName} database.")
            else:
                print(f"Collection {collectionName} does not exist in {dbName} database.")
        else:
            print(f"Database {dbName} does not exist.")
           
    def checkExist(self):
        if self.db.name in self.client.list_database_names():
            if self.collection.name in self.db.list_collection_names():
                return True
        return False

    def isEmbeded(self):
        tmp = self.collection.count_documents({"embedding": { "$exists": 1 }})
        if tmp != 0:
            return True
        else:
            return False
        
    def semanticSearch(self, text,returnHeader, n = 1):
        """return a table (list of list) with returnHeader as column and n as numbers of row, sorted by similarity"""
        text_vec = get_embedding(text, engine="text-embedding-ada-002")
        df = pd.DataFrame(list(self.collection.find()))
        
        df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, text_vec))
        
        result = []
        for i in range(0,n):
            """return the value of embeded field"""
            result.append(df.sort_values("similarities", ascending=False, ignore_index =True).iloc[i][returnHeader].tolist())
        return result
            


