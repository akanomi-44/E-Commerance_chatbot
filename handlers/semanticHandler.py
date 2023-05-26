import json
import httpx
import pandas as pd
import asyncio
import openai
from openai.embeddings_utils import cosine_similarity
from db.mongo import db
from config import Config

openai.api_key = Config.OPENAI_API_KEY

class semanticCollection:
    def __init__(self,  embField):
        self.embField = embField
    
    # def addData(self,data: list):
    #     '''List of dict as input'''
    #     self.collection.insert_many(data)
    # 
    # def printData(self):
    #     for item in self.collection.find():
    #         print(item)
    #
    # def toDF(self):
    #     df = pd.DataFrame(list(self.collection.find()))
    #     return df
    #
    # def embeddingData(self,field):
    #     '''Add embeded value of req'''
    #     if self.embField != field:
    #         self.embField = field
    #         
    #     df = pd.DataFrame(list(self.collection.find()))
    #     df['embedding'] = df[field].apply(lambda x: get_embedding(x , engine='text-embedding-ada-002'))
    #     
    #     for doc in self.collection.find():
    #         embedding = df.loc[df['_id'] == doc['_id'], 'embedding'].values[0]
    #         
    #         self.collection.update_one({'_id': doc['_id']}, {'$set': {'embedding': embedding}})
    
    # def semanticSearch(self, text,returnHeader, n = 1):
    #     """return a table (list of list) with returnHeader as column and n as numbers of row, sorted by similarity"""
    #     text_vec = get_embedding(text, engine="text-embedding-ada-002")
    #     df = pd.DataFrame(list(self.collection.find()))
        
    #     df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, text_vec))
        
    #     result = []
    #     for i in range(0,n):
    #         """return the value of embeded field"""
    #         result.append(df.sort_values("similarities", ascending=False, ignore_index =True).iloc[i][returnHeader].tolist())
    #     return result

    async def get_embeddings(self, text):
        url = "https://api.openai.com/v1/embeddings"
        
        payload = json.dumps({
        "input": text,
        "model": "text-embedding-ada-002"
        })
        headers = {
        'Authorization': 'Bearer ' + Config.OPENAI_API_KEY,
        'Content-Type': 'application/json'
        }
        async with httpx.AsyncClient() as client:
            async with session.post(url, data=payload, headers=headers) as response:
                result = await response.json()
                return result


    async def semanticSearch(self, text,returnHeader, n = 1):
        """return a table (list of list) with returnHeader as column and n as numbers of row, sorted by similarity"""
        results = await asyncio.gather(self.get_embeddings(text=text), db.find_documents('templateReq',{}))

        embedding_data, docs = results
        df = pd.DataFrame(docs)

        if 'error' in  embedding_data:
            if embedding_data['error']['code'] == 'invalid_api_key':
                raise PermissionError("Invalid Open Ai Key")    
            if 'message' in embedding_data['error']:
                raise ConnectionError( embedding_data['error']['message'])
            raise TypeError( embedding_data['error']['code'])
        
        text_vec = embedding_data['data'][0]['embedding']
        df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, text_vec))
        
        result = []
        for i in range(0,n):
            """return the value of embeded field"""
            result.append(df.sort_values("similarities", ascending=False, ignore_index =True).iloc[i][returnHeader].tolist())
        return result
