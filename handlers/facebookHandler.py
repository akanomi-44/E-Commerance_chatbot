import requests
import hmac
import hashlib

from .requestHandler import handle_case1, handle_case3, handle_case2, handle_default
from .semanticHandler import semanticCollection 

from config import Config

from db.mongo import pagesCollection

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
    


def verify_signature(signature, payload):
    expected_signature = 'sha1=' + hmac.new(Config.APP_SECRET.encode(), payload, hashlib.sha1).hexdigest()
    print(expected_signature)
    return hmac.compare_digest(signature, expected_signature)


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



def send_message(recipient_id, page_id , text ):
    """Send a response to Facebook"""
    payload = {
        "messaging_type": "RESPONSE",
        "message":{
            "text":text
        },
        "recipient": {
            'id': recipient_id
        }
    }   
    
    page = pagesCollection.find_one({'page_id': page_id})
    if not page:
       return
    access_token = page['access_token']

                
    auth = {
        'access_token': access_token,
    }

    response = requests.post(
        f"https://graph.facebook.com/v16.0/{page_id}/messages",
        params=auth,
        json=payload
    )

    return response.json()


def handle_facebook_message(recipient_id, sender_id, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    # DONE: Add a classify function
    requtest_type = request_classifyer(message)
    print(f"type {requtest_type}")
    match requtest_type:
        case "case_1":
            response = handle_case1(message)
            return send_message(recipient_id , sender_id, response)
        case "case_2":
            response = handle_case2(message)
            return send_message(recipient_id , sender_id, response)
        case "case_3":
            response = handle_case3(message)
            return send_message(recipient_id , sender_id, response)
        case "default":
            response = handle_default(message)
            return send_message(recipient_id , sender_id, response)
    
    response = "Error: An unexpected error has occurred."
    return send_message(recipient_id , sender_id, response)
    # response = get_bot_response(message)
    # if(response):    
    #     return send_message(sender_id,recipient_id, response)
    # return handle_chatgpt_message(sender_id, message)


