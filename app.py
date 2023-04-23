from flask import Flask, request
from handlers.facebookHandler import verify_webhook, is_user_message, respondHandler
from handlers.authHandler import login, register
import os
app = Flask(__name__)


app.route('/login', methods=['POST'])
def login():
    return login(request)



app.route('/register', methods=['POST'])
def register():
    return register(request)


@app.route("/webhook", methods=['GET', 'POST'])
def listen():
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
                respondHandler(sender_id, text)

        return "ok"
    
