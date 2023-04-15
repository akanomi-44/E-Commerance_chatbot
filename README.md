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
### place an order
redirect user to e-comerance platform 
### Check product availability
check if product is in stock

## Testing:
1. check/uncheck option in ```test_db_prep.py``` (if run it first time set all if to 1)
**NOTE**: after first run, set all if case to 0. Only change when needed
2. edit template at line 50 of ```test_db_prep.py``` if needed
3. run ```test_driver.py```

## TODO:
- [x] Find best suitable template request
- [x] Add more testcase 
- [x] Request handle
- [ ] Restrict to clothings consultation
- [x] Automate testing process
