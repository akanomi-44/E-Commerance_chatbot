from flask import Flask, request
import hmac
import hashlib
import db_helper as db

import requests

from dotenv import load_dotenv

from handlers.chatgptHandler import handle_chatgpt_message

import os
app = Flask(__name__)


load_dotenv()

APP_SECRET = os.getenv("APP_SECRET")
FB_API_URL = os.getenv("FB_API_URL")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

appsecret_proof = hmac.new(
    APP_SECRET.encode('utf-8'),
    PAGE_ACCESS_TOKEN.encode('utf-8'),
    hashlib.sha256
).hexdigest()

##server
server = db.Server("Store","templateReq")

def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    #return "This is a dummy response to '{}'".format(message)
    ressult = server.semanticSearch(message,["case_no"])
    return "Your request is in {}".format(ressult[0][0])


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    if(response):    
        send_message(sender, response)
    else :
        handle_chatgpt_message(message)


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route("/webhook", methods=['GET', 'POST'])
def listen():
    print(request)
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        print("Post Payload: ", payload)
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)

        return "ok"
        
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
        'access_token': PAGE_ACCESS_TOKEN,
        'appsecret_proof': appsecret_proof
    }

    response = requests.post(
        f"https://graph.facebook.com/v16.0/{PAGE_ID}/messages",
        params=auth,
        json=payload
    )
    return response.json()