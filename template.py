# ADD template to db server
import db_helper as db
from config import Config


host = Config.DB_CLUSTER
userName = Config.DB_USER_NAME
password = Config.DB_PASS
uri = f"mongodb+srv://{userName}:{password}@{host}/?retryWrites=true&compressors=zlib"


def templateRead(name):
    inputData = []
    with open(name, "r") as open_file:
        inputData = open_file.read().splitlines()
    toDict = [
        {"req": req, "case_no": case}
        for req, case in (item.split(";") for item in inputData)
    ]

    for id, item in enumerate(toDict):
        item["id"] = id
    return toDict


if __name__ == "__main__":
    # template
    print(uri)
    template_server = db.Server(dbName="Store", collectionName="templateReq",clientName=uri)
    template_server.embField = "req"
    if 1:
        if 1:
            template_server.dropCollection()

        if 1:
            templateData = templateRead("./template/template.txt")
            template_server.addData(templateData)

        if 1:
            template_server.embeddingData("req")

        if 1:
            print((template_server.toDF()))