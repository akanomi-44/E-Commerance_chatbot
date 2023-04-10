from itertools import count
from os.path import exists
import pymongo
import pandas as pd
import openai
import APIkey
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity

openai.api_key = APIkey.get_key()

#default client (local host)
client = pymongo.MongoClient("mongodb://localhost:27017/")

class Server:
    def __init__(self,dbName, collectionName, clientName= "mongodb://localhost:27017/", ):
        self.client = pymongo.MongoClient(clientName)
        self.db = self.client[dbName]
        self.collection = self.db[collectionName]
    
    def addData(self,data: list):
        self.collection.insert_many(data)
    
    def printData(self):
        for item in self.collection.find():
            print(item)

    def embeddingData(self,field=None):
        '''Add embeded value of req'''
        if field is None:
            print("field can not be None")
        else:
            self.embField = field
            df = pd.DataFrame(list(self.collection.find()))
            df['embedding'] = df[field].apply(lambda x: get_embedding(x , engine='text-embedding-ada-002'))
            
            for doc in self.collection.find():
                embedding = df.loc[df['id'] == doc['id'], 'embedding'].values[0]
                
                self.collection.update_one({'_id': doc['_id']}, {'$set': {'embedding': embedding}})


        # tmp
            df.to_csv("tmp.csv")
        # for _,row in df.iterrows():
        #     print(type(row.get('embedding')))
    
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
            
    def semanticSearch(self,text = None):
        if text is None:
            return 
        else:
            text_vec = get_embedding(text, engine="text-embedding-ada-002")
            
            df = pd.DataFrame(list(self.collection.find()))
            
            # Transform data from string to numpy array in order to calculate 
            # df['embedding'] = df['embedding'].apply(eval).apply(np.array)

            df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, text_vec))

            if 0: 
                print("======================================================================")
                print(df[[self.embField,"similarities"]].sort_values("similarities", ascending=False))
                print("======================================================================")
            if 1:
                # return df.loc[:][self.embField]
                return df[[self.embField,"similarities"]].sort_values("similarities", ascending=False, ignore_index =True)[:][self.embField]

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
    
    def getMostRelavant(self,text):
        if text is None:
            return 
        else:
            text_vec = get_embedding(text, engine="text-embedding-ada-002")
            
            df = pd.DataFrame(list(self.collection.find()))
            
            # Transform data from string to numpy array in order to calculate 
            # df['embedding'] = df['embedding'].apply(eval).apply(np.array)

            df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, text_vec))

            if 1: 
                print("===================================================")
                print(df[[self.embField,"similarities"]].sort_values("similarities", ascending=False))
                print("===================================================")
            if 1:
                # print(df[[self.embField,"similarities"]].sort_values("similarities", ascending=False, ignore_index=True).loc[0][self.embField])
                return df[[self.embField,"similarities"]].sort_values("similarities", ascending=False, ignore_index=True).loc[0][self.embField]

