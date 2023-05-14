import requests
import hmac
import hashlib

from .requestHandler import handle_case1, handle_case3, handle_case2, handle_default
from .semanticHandler import semanticCollection 

from config import Config



def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    #return "This is a dummy response to '{}'".format(message)

def request_classifyer(message):
    col = semanticCollection("templateReq","req") 
    result = col.semanticSearch(message,["case_no","similarities"])
    # print(result)
    if result[0][1] >= 0.82:
        case_mapping = {
            "case1_recommendation": "case_1",
            "case2_placeOrder": "case_2",
            "case3_conntactHuman": "case_3"
        }
        case_no = result[0][0]
        if case_no in case_mapping:
            return case_mapping[case_no]
        else:
            return "default"
    else:
        return "default"
    


def verify_webhook(req):
    if req.args.get("hub.verify_token") == Config.VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))



def send_message(recipient_id,sender_id, message):
    """Send a response to Facebook"""
    payload = {
        "messaging_type": "RESPONSE",
        "message":{
            "text":message
        },
        "recipient": {
            'id': recipient_id
        }
    }

    # page_info = 
    
    appsecret_proof = hmac.new(
    Config.APP_SECRET.encode('utf-8'),
    Config.PAGE_ACCESS_TOKEN.encode('utf-8'),
    hashlib.sha256
    ).hexdigest()

    auth = {
        'access_token': Config.PAGE_ACCESS_TOKEN,
        #'appsecret_proof': appsecret_proof
    }

    response =  requests.post(
        f"https://graph.facebook.com/v16.0/{sender_id}/messages",
        params=auth,
        json=payload
    )
    return response.json()



def handle_facebook_message(sender_id,recipient_id,  message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    # DONE: Add a classify function
    requtest_type = request_classifyer(message)
    print(f"type {requtest_type}")
    match requtest_type:
        case "case_1":
            response = handle_case1(message)
            return send_message(sender_id, response)
        case "case_2":
            response = handle_case2(message)
            return send_message(sender_id, response)
        case "case_3":
            response = handle_case3(message)
            return send_message(sender_id, response)
        case "default":
            response = handle_default(message)
            return send_message(sender_id, response)
    
    response = "Error: An unexpected error has occurred."
    return send_message(sender_id, response)
    # response = get_bot_response(message)
    # if(response):    
    #     return send_message(sender_id,recipient_id, response)
    # return handle_chatgpt_message(sender_id, message)


