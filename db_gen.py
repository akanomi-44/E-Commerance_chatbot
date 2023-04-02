import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mydatabase"]
mycol = mydb["customer req"]
mycol.drop()

if __name__ == "__main__":
    data = [
        {"req": "buy blue shirt", "action": "do somethings"},
        {"req": "print receipt", "action": "do somethings"},
        {"req": "get more infomation", "action": "do somethings"},
    ]

    x = mycol.insert_many(data)
