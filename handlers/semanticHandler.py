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
            response= await client.post(url, data=payload, headers=headers)
            return response.json()        

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
