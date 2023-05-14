from flask import Flask, request, jsonify, render_template
import hmac
import hashlib

import requests
app = Flask(__name__)
from pymongo import MongoClient
from config import Config
from db.mongo import client
import os
from dotenv import load_dotenv
import certifi
import urllib3

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

# appsecret_proof = hmac.new(
#     APP_SECRET.encode('utf-8'),
#     PAGE_ACCESS_TOKEN.encode('utf-8'),
#     hashlib.sha256
# ).hexdigest()

db = client['Store']
collection = db['pages']


def has_valid_ssl(domain):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )
    try:
        response = http.request('GET', domain)
        if response.status == 200:
            return True
        else:
            return False

    except urllib3.exceptions.SSLError:
        return False
    except urllib3.exceptions.HTTPError:
        return False
    except urllib3.exceptions.RequestError:
        return False

def verify_signature(signature, payload):
    expected_signature = 'sha1=' + hmac.new(APP_SECRET.encode(), payload, hashlib.sha1).hexdigest()
    print(expected_signature)
    return hmac.compare_digest(signature, expected_signature)


def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    return "This is a dummy response to '{}'".format(message)
from functools import wraps
from flask import Flask, jsonify, request, render_template
import jwt
from handlers.facebookHandler import verify_webhook, is_user_message, handle_facebook_message
from handlers.authHandler import login, register
from config import  Config

from dotenv import load_dotenv
app = Flask(__name__)


load_dotenv()

# APP_ID = os.getenv("APP_ID")
# APP_SECRET = os.getenv("APP_SECRET")
# FB_API_URL = os.getenv("FB_API_URL")
# VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
# CALLBACK_URL = os.getenv("CALLBACK_URL")
# PAGE_INFO = dict()
# PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
# PAGE_ID = os.getenv("PAGE_ID")
# APP_TOKEN = os.getenv("APP_TOKEN")

# ADD_PAGE_URL = 'https://graph.facebook.com/{APP_ID}/subscriptions?access_token=969470277523176%7Cpvw0lLU3YmoSQ0l4aFx3G118vJw'


app.config['SECRET_KEY'] = Config.SECRET_KEY


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))



def send_message(recipient_id, text, page_id):
    print("")
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
    access_token = ""
    result = collection.find_one({'page_id': page_id})
    access_token = result['access_token']

    print("access_token: ", access_token)
                
    auth = {
        'access_token': access_token,
    }

    response = requests.post(
        f"https://graph.facebook.com/v16.0/{page_id}/messages",
        params=auth,
        json=payload
    )
    print("respond", response)
    print("json", response.json())
    return response.json()

@app.route("/add_page_info", methods=['POST'])
def set_page_info():
    if request.method == 'POST':
        PAGE_ACCESS_TOKEN = request.json.get("page_access_token")
        PAGE_ID = request.json.get("page_id")
        user_id = request.json.get("user_id")
        
        url = f'https://graph.facebook.com/v16.0/{PAGE_ID}/subscribed_apps'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'app_id': APP_ID,
            'subscribed_fields': 'messages',
            'access_token': PAGE_ACCESS_TOKEN 
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            result = collection.find_one({'page_id': PAGE_ID})
        

            print(result)
            if result is None:
                collection.insert_one({
                    'page_id': PAGE_ID,
                    'user_id': user_id,
                    'access_token': PAGE_ACCESS_TOKEN,
                    'webhook': ''
                })
            else:
                collection.update_one({'page_id': PAGE_ID}, {'$set': {'access_token': PAGE_ACCESS_TOKEN}})
            return jsonify({"message": "Page info added successfully."}), 200
        else:
            jsonify({"error": "Add page failed."}), 400
       
        
    else:
        return jsonify({"error": "Unsupported request method."}), 400

@app.route("/webhook", methods=['GET', 'POST'])
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        print("Verify token: ", VERIFY_TOKEN)
        return verify_webhook(request)

    if request.method == 'POST':
        signature = request.headers.get('X-Hub-Signature')
        payload = request.get_data()
        if not verify_signature(signature, payload):
            return jsonify({"error": "Unsupported request method."}), 400
        payload = request.json
        print("Post Payload: ", payload)
        result = collection.find_one({'page_id': payload['entry'][0]['id']})
        print("result: ", result)
        if result is None:
            print('No document found with page_id', payload['entry'][0]['id'])
            return jsonify({"error": "Page Id is not registereds."}), 401

        event = payload['entry'][0]['messaging']
        page_id = payload['entry'][0]['id']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                print("entering respond:")
                respond(sender_id, text, page_id)

                
        return "ok"

@app.route('/set_webhook_url', methods=['POST'])
def set_webhook_url():
    page_webhook_url = request.json.get("page_webhook_url")
    page_id = request.json.get("page_id")
    if not has_valid_ssl(page_webhook_url):
       return jsonify({"error": "Insecure request. Please use HTTPS."}), 400
    
    query = {'page_id': page_id}
    document = collection.find_one(query)
    if document:
        document['webhook'] = page_webhook_url
        collection.update_one(query, {'$set': document})
    else: 
        return jsonify({"error": "Page Id not exist in database."}), 400
    
    return jsonify({"message": "Add successfully."}), 200
    
@app.route('/getWebhooks', methods=['GET'])
def getWebhooks():
    user_id = request.args.get('user_id')

    query = {'user_id': user_id}
    document = collection.find(query)
    if document: 
        return jsonify(document), 200
    
    return jsonify({"error": "user_id not exist in database."}), 400
    

@app.route('/html')
def index():
    return render_template('facebook_login.html')

def main():
    app.run()


if __name__ == "__main__":
    main()