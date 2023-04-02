import pymongo
import openai
import pandas as pd
import numpy as np
import APIkey
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity




openai.api_key = APIkey.get_key()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customer req"]

def CalEmbeding():
    # temp: export database into csv file
    # TODO: add new prop to database as string type
    df = pd.DataFrame(list(mycol.find()))
    df['embedding'] = df['req'].apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))
    df.to_csv('word_embeddings.csv')

def CalSimilarity(cus_req_vec):
    # temp: Take data from csv file
    # TODO: Take data from database
    df = pd.read_csv('word_embeddings.csv')

    # Transform data from string to numpy array in order to calculate 
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)

    df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, cus_req_vec))

    # temp: print and sort data here
    print(df.sort_values("similarities", ascending=False)['req'])

def handleReq(cus_req):
    cus_req_vec = get_embedding(cus_req, engine="text-embedding-ada-002")
    CalSimilarity(cus_req_vec)

if __name__ == "__main__":
    # CalEmbeding() # Embedding request data
    cus_req = "bill details"
    handleReq(cus_req)