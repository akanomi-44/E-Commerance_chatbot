import db_helper as db


def inputRead(name, caseNo):
    inputData = []
    with open(name, "r") as open_file:
        inputData = open_file.read().splitlines()
    toDict = [{"id":id, "req": req, "case_no":caseNo} for id,req in enumerate(inputData)]
    return toDict

def templateRead(name):
    inputData = []
    with open(name, "r") as open_file:
        inputData = open_file.read().splitlines()
    toDict = [{"req": req, "case_no":case} for req,case in (item.split(";") for item in inputData)]

    for id,item in enumerate(toDict):
        item["id"] = id
    return toDict

if __name__ == "__main__":
    #customer req database 
    server = db.Server(dbName="Store",collectionName="cusReq")
    server.embField = "req"
    
    if 0: 
        server.dropCollection()
        
    if 0:
        case1_data = inputRead("./cases/test_case1.txt","Case1-consultation")
        case2_data = inputRead("./cases/test_case2.txt","Case2-availability")
        case3_data = inputRead("./cases/test_case3.txt","Case3-order")
        server.addData(case1_data)
        server.addData(case2_data)
        server.addData(case3_data)
        
    if 0:
        server.embeddingData("req")

    if 0:
        print((server.toDF()))

    #template
    template_server = db.Server(dbName="Store", collectionName="templateReq")
    template_server.embField = "req"
    if 1: 
        template_server.dropCollection()
        
    if 1:
        templateData = templateRead("./template/template1.txt")
        template_server.addData(templateData)
        
    if 1: 
        template_server.embeddingData("req")

    if 1:
        print((template_server.toDF()))
