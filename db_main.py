import db_helper as sv

reqData =[ 
    {"id": '1', "req": "product consultation", "action": "begin product consultation/advice"},
    {"id": '2', "req": "make a complaint about the product", "action": "contact store owner"},
    {"id": '3', "req": "place an order", "action": "redirect to E-commerce platform"},
    {"id": '4', "req": "contact human assistant", "action": "contact store owner"},
    {"id": '5', "req": "Check product availability", "action": "check database"},
]

cusReqData = [
        {
            "id" : 1,
            "userId": 'id1',
            "req":"Hi, I'm looking for a new outfit for a job interview. Can you help me find something professional but also stylish?",
            "res":"Hello! Of course, I'd be happy to help you find something that will make a great impression on your interview. What kind of position are you interviewing for?"
        },
        {
            "id" : 2,
            "userId": 'id1',
            "req":"It's for a marketing position at a startup company. So, I want to look professional but not too formal.",
            "res":"Understood. We have a wide selection of clothing that could fit your needs. Have you considered wearing a blazer with a nice pair of pants or a skirt?"
        },
        {
            "id" : 3,
            "userId": 'id1',
            "req":"Yes, I've thought about it. What do you suggest?",
            "res":"For a professional but stylish look, I suggest a black blazer paired with either a pair of black dress pants or a knee-length black skirt. You could also add a pop of color with a blouse or shirt in a light blue or pink shade. How does that sound?"
        },
        {
            "id" : 4,
            "userId": 'id1',
            "req":"That sounds great! Do you have any specific blazers or pants in mind that you can show me?",
            "res":"Absolutely! Here are a few options. <show options>"
        },
        {
            "id" : 5,
            "userId": 'id1',
            "req":"Hi, I'm looking for a new outfit for marketing position job interview at a startup company. Can you help me find something professional but also stylish?",
            "res":"For a professional but stylish look, I suggest a black blazer paired with either a pair of black dress pants or a knee-length black skirt. You could also add a pop of color with a blouse or shirt in a light blue or pink shade.Here are a few options <list options from shop db>"
        },
        ]
if __name__ == "__main__":
    templateReq = sv.Server(dbName="Store",collectionName="reqTemplate")

    if 0:
        templateReq.dropCollection()
        
    if 0:
        templateReq.addData(reqData)
    
    if not templateReq.isEmbeded(): #run once
        templateReq.embeddingData("req")
    
    if 0:
        templateReq.embField = "req"
        userInput = str(input("How can i help you today: "))
        templateReq.semanticSearch(userInput)

    # if 0: #process req 
    #     server = sv.Server(dbName="Store",collectionName="cusReqEmb")
    #     server.dropCollection()
    #     server.addData(cusReqData)
    #     server.embeddingData("req")
