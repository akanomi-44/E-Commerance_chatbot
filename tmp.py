import db_helper as db

def printDF(df, returnVlue = [], n = 3):
    print("======================================================================")
    # print(df[returnVlue].sort_values("_id", ascending=False).head(n))
    # print(df[returnVlue].sort_values("_id", ascending=False).iloc[:n])
    print(df.sort_values("_id", ascending=False)[:n][returnVlue])
    print("======================================================================")
        
def returnListFromDF(df, returnVlue = [], n = 3):
    result = []
    for i in range(0,n):
        result.append(df.sort_values("id", ascending=False).iloc[i][returnVlue].tolist())

    return result

if __name__ == "__main__":
    server = db.Server("Store","templateReq")
    
    df = server.toDF()
    # for item in returnListFromDF(df,"req",5):
    #     print(item)
    #     print("==========")
    x = returnListFromDF(df,["req","id"],5)
    for item in x:
        print(item)


    
