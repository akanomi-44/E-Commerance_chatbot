
import requests
import hmac
import hashlib

from handlers.requestHandler import handle_case1, handle_case3
from .semanticHandler import semanticCollection 

from .chatgptHandler import get_gpt3_response, handle_chatgpt_message

from .userHandler import applyFunction, case1_recommendation, case2_placeOrder, case3_conntactHuman
#DONE: add import for request handler

from config import Config

appsecret_proof = hmac.new(
    Config.APP_SECRET.encode('utf-8'),
    Config.PAGE_ACCESS_TOKEN.encode('utf-8'),
    hashlib.sha256
).hexdigest()

def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    #return "This is a dummy response to '{}'".format(message)

def request_classifyer(message):
    col = semanticCollection("classifyReq","req") 
    result = col.semanticSearch(message,["case","similarities"])
    if result[0][1] >= 0.82:
        match result[0][0]:
            case "case1_recommendation":
                return "case_1"
            case "case2_placeOrder":
                return "case_2"
            case "case3_conntactHuman":
                return "case_3"
            case default:
                return "denied"
    else:
        return "denied"
    


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



def send_message(recipient_id, message):
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

    auth = {
        'access_token': Config.PAGE_ACCESS_TOKEN,
        'appsecret_proof': appsecret_proof
    }

    response =  requests.post(
        f"https://graph.facebook.com/v16.0/{Config.PAGE_ID}/messages",
        params=auth,
        json=payload
    )
    return response.json()



def handle_facebook_message(sender_id, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    # DONE: Add a classify function
    requtest_type = request_classifyer(message)
    
    match requtest_type:
        case "case_1":
            response = handle_case1(message)
            return send_message(sender_id, response)
        case "case_2":
            # TODO now: handle this case
            return 
        case "case_3":
            response = handle_case3(message)
            return send_message(sender_id, response)
        case "denied":
            response = "Chatbot currently can't not process this request" 
            return send_message(sender_id, response)
            
    
    
    # if(response):    
    #     return send_message(sender_id, response)
    # return handle_chatgpt_message(sender_id, message) #TODO: turn this into reject request


