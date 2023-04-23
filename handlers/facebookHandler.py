
import requests
import hmac
import hashlib

from chatgptHandler import handle_chatgpt_message

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
    result = server.semanticSearch(message,["case_no"])
    return "Your request is in {}".format(result[0][0])


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

    response = requests.post(
        f"https://graph.facebook.com/v16.0/{Config.PAGE_ID}/messages",
        params=auth,
        json=payload
    )
    return response.json()



def respondHandler(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    if(response):    
        send_message(sender, response)
    else :
        handle_chatgpt_message(message)
