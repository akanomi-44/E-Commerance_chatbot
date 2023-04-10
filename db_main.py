import db_helper as sv

reqData =[ 
    {"id": '1', "req": "assist with product selection", "action": "begin product consultation/advice"},
    {"id": '2', "req": "make a complaint about the product", "action": "contact store owner"},
    {"id": '3', "req": "place an order", "action": "redirect to E-commerce platform"},
    {"id": '4', "req": "contact manager", "action": "contact store owner"},
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

def demo(sv: sv.Server):
    # tmp
    sv.embField = "req"
    index = 0
    # /tmp
    
    print("ChatBot: How can i help you today ?")
    # userInput = str(input("How can i help you today: "))
    userInput = "Hi, I'm looking for a new outfit. Can you help me ?"
    # userInput = "Hi, I'm having some problem with the shirt i bought recently"
    # userInput = "is this shirt available ?"
    print(f"User: {userInput}")
    res = sv.semanticSearch(userInput)

    while True:
        print(f"ChatBot: Do you want to {res[index]} [y/n]")
        userInput = str(input("User: "))
        if index == len(res):
            break
        if userInput == 'n':
            index += 1
        else:
            break

    if userInput == 'y': 
        print(f"ChatBot: OK! I'm on it")
    else:
        print(f"ChatBot: Sorry i can not process your request. I'll contact the manager")
    
    
    #Todo: return list in order to check for each option

if __name__ == "__main__":
    templateReq = sv.Server(dbName="Store",collectionName="reqTemplate")

    if 0:
        templateReq.dropCollection()
        
    if 0:
        templateReq.addData(reqData)
    
    if not templateReq.isEmbeded(): #run once
        templateReq.embeddingData("req")
        print("===DONE EMBEDDING DATA===")
    
    if 0:
        templateReq.embField = "req"
        userInput = str(input("How can i help you today: "))
        templateReq.semanticSearch(userInput)

    demo(templateReq)
    # if 0: #process req 
    #     server = sv.Server(dbName="Store",collectionName="cusReqEmb")
    #     server.dropCollection()
    #     server.addData(cusReqData)
    #     server.embeddingData("req")
