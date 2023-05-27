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

    # if 1:
    #     #userInput = ""
    #     #userInput = "I'm in search of a dress to wear to a wedding this summer. Do you have any recommendations for something that's both elegant and comfortable?"
    #     #userInput = "Your faith was strong but you needed proof, You saw her bathing on the roof"
    #     #userInput = "Can i contact an employee ?"
    #     userInput = "Snake is a type of cow"
    #     for line in template_server.semanticSearch(userInput,["case_no","similarities","req"],5):
    #         print(line)

    if 0:
        user_requests = [
            "Can you recommend a good book for me to read?",
            "How do I fix a leaking faucet?",
            "What's the best way to learn a new language?",
            "Can you recommend a good restaurant in the area?",
            "What's the weather forecast for tomorrow?",
            "How can I improve my public speaking skills?",
            "What are some good workout routines for beginners?",
            "What's the best way to study for an exam?",
            "Can you recommend a good movie to watch tonight?",
            "How can I troubleshoot a problem with my computer?",
        ]

        for request in user_requests:
            print("="*10 + request)
            for line in template_server.semanticSearch(request,["case_no","similarities","req"],5):
                print(line)

    if 1:
        print((template_server.toDF()))

