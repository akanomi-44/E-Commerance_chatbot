import db_helper as db

if __name__ == "__main__":
    server = db.Server("Store", "templateReq")
    userInput = "I'm not sure what to wear for weedding. Can you help me find something suitable?"
    result = server.semanticSearch(userInput,["case_no","similarities"],3)
    for row in result:
        print(row)

    print(result[0][0])
