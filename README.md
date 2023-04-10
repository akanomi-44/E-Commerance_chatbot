# Apply chatGPT into Facebook's chatbot for e-comerance

## Usage flow
1. System: "How can i help you to day? "
2. User sends a request ```req```
3. Process ```req``` and find most relevent template request from database(using semantic search) and confirm it with User
4. User confirms request and System start processing user's ```req```

## Template request
### Product consultation
Case 1: short and few request: <br>
    combine old promt and new ```req``` into new prompt and send to openaiAPI <br>
Case 2: many requests <br>
    Use semantic search and select most relevent requests and make them into context. Send new ```req``` with context to openaiAPI <br>
### make a complaint about the product
sys: Ask for order infomation ? -> check order information -> send notification to store's owner
### place an order
redirect user to e-comerance platform 
### contact human assistant
send notification to store's owner
### Check product availability
check if product is in stock

## TODO:
- [ ] Find best suitable template request
- [ ] Add more testcase 
- [ ] Request handle
- [ ] Restrict to clothings consultation

