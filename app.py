
import asyncio
from bson import json_util
import json

from functools import wraps
from flask import Flask, g, request, jsonify
import jwt
import requests
from config import Config
from db.mongo import db
from dotenv import load_dotenv
from flask_cors import CORS

from handlers.facebookHandler import handle_facebook_message, is_user_message, send_message, verify_signature, verify_webhook
from handlers.sslHandler import has_valid_ssl

app = Flask(__name__)
cors = CORS(app)

load_dotenv()


def token_user_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        tokenBearer = request.headers.get('Authorization')
        if not tokenBearer:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            token =tokenBearer.split(' ')[1]
            data = jwt.decode(token, algorithms="HS256",key= Config.JWT_SECRET_KEY)
            g.user_id = data['user_id']
        except Exception as e:
            print(e)
            return jsonify({'message': 'Token is invalid!'}), 401

        return await f(*args, **kwargs)

    return decorated



def token_webhook_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        tokenBearer = request.headers.get('Authorization')
        if not tokenBearer:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            token =tokenBearer.split(' ')[1]
            data = jwt.decode(token, algorithms="HS256",key= Config.JWT_SECRET_KEY)
            g.page_id = data['page_id'] 
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return await f(*args, **kwargs)

    return decorated

@app.route('/send_message', methods=['POST'])
@token_webhook_required
async def webhook_send_message():
    page_id = g.page_id

    text= request.json['text']
    user_id =request.json['user_id']
    print(text, user_id)
    try:
        page = await db.find_one_document("pages", {'page_id': page_id})
        if not page:
          return
        
        access_token = page['access_token']        

        send_message(recipient_id=user_id, page_id=page_id, text=text,access_token=access_token)
        return jsonify({"ok: true"}), 200
    except Exception as e:
        print(e) 
        return jsonify({'message': 'Internal server error'}), 503

@app.route("/add_page_info", methods=['POST'])
@token_user_required
async def set_page_info():

    body = json.loads(request.json.get("body"))
    PAGE_ACCESS_TOKEN = body['page_access_token']
    PAGE_ID = body['page_id']
    user_id = g.user_id 
    
    url = f'https://graph.facebook.com/v16.0/{PAGE_ID}/subscribed_apps'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'app_id': Config.APP_ID,
        'subscribed_fields': 'messages',
        'access_token': PAGE_ACCESS_TOKEN 
    }
    try:
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            result = await db.find_one_and_update("pages", {'page_id': PAGE_ID} ,{'$set':{
                    'page_id': PAGE_ID,
                    'user_id': user_id,
                    'access_token': PAGE_ACCESS_TOKEN,
                    'webhook': ''
                }}, upsert=True)
            if result:
                return jsonify({"message": "Page info added successfully."}), 200
        print(response.json())
        return jsonify({"error": "Failed to install app"}), 400
    except Exception as e: 
        print(e)
        return jsonify({"error":"fail"}), 400

@app.route("/webhook", methods=['GET', 'POST'])
async def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    try: 
        if request.method == 'GET':
            return verify_webhook(request)

        if request.method == 'POST':
            signature = request.headers.get('X-Hub-Signature')
            payload = request.get_data()
            if not verify_signature(signature, payload):
                return jsonify({"error": "Unsupported request method."}), 400
            payload = request.json
            
            for entry in payload['entry']:
                page_id = entry['id']
                for event in entry['messaging']:
                    if is_user_message(event):
                        text = event['message']['text']
                        sender_id = event['sender']['id']
                        await handle_facebook_message(sender_id,page_id, text )

        return jsonify({'ok':True}),200
    except Exception as e:
        print(e)
        return jsonify({'ok':False}),500

@app.route('/set_webhook_url', methods=['POST'])
@token_user_required
async def set_webhook_url():
    body = json.loads( request.json.get("body"))
    page_webhook_url = body["page_webhook_url"].strip()
    page_id = body["page_id"].strip()
    res  =has_valid_ssl(page_webhook_url)

    if not res:
       return jsonify({"error": "Insecure request. Please use HTTPS."}), 400
    
    document = await db.find_one_and_update("pages",{'page_id': page_id}, {'$set': {"webhook": page_webhook_url}}, upsert=False)
    if not document: 
        return jsonify({"error": "Page Id not exist in database."}), 400
    
    token = jwt.encode(
                {'page_id': page_id, 'page_webhook_url': page_webhook_url},
                Config.JWT_SECRET_KEY,
                algorithm='HS256'
            )
    return jsonify({'token': token}), 200
    
@app.route('/getWebhooks', methods=['GET'])
@token_user_required
async def getWebhooks():
    try: 
        user_id = g.user_id
        client,document = await asyncio.gather(db.find_one_document('clients', {'client_id': user_id}),db.find_documents('pages',{'user_id': user_id}))
        if not client:
            return jsonify({"error": "user_id not exist in database."}), 400  
        if not document:
            return jsonify({"ok": "true", "pages": []}), 200

        return jsonify({'pages':json.loads(json_util.dumps(document))}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/auth/facebook', methods =['POST'])
async def loginUser():
    access_token = request.json.get("access_token")
    url = f'https://graph.facebook.com/v16.0/me?access_token={access_token}&fields=id,name'
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers).json()
        user_id = response['id']
        name = response['name']
        data =  await db.find_one_and_update("clients",{"client_id": user_id}, {"$set": {"client_id": user_id, "name": name}}, upsert=True)
        if data: 
            token = jwt.encode(
                    {'user_id': user_id, 'name': name},
                    Config.JWT_SECRET_KEY,
                    algorithm='HS256'
                )
            return jsonify({'token': token}), 200
        return jsonify({'message': 'Authentication failed'}), 401
    except Exception as e:
        print(e)
        return jsonify({'message': 'Authentication failed'}), 401


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)