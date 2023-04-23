from flask import Flask, request
from handlers.facebookHandler import verify_webhook, is_user_message, handle_facebook_message
from handlers.authHandler import login, register

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
        entries =payload['entry'] 
        
        for entry in entries:
            events = entry['messaging']
            for event in events:
                if is_user_message(event):
                    text = event['message']['text']
                    sender_id = event['sender']['id']
                    handle_facebook_message(sender_id, text)

        return "ok"
    
