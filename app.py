
import asyncio
from bson import json_util
import json

from functools import wraps
import jwt
from quart_cors import cors
from config import Config
from db.mongo import db
from dotenv import load_dotenv

from handlers.facebookHandler import get_facebook_user, handle_facebook_message, is_user_message, send_message, subscribe_app, verify_signature, verify_webhook
from handlers.sslHandler import has_valid_ssl
from quart import Quart, g, jsonify, request
app = Quart(__name__)
CORS = cors(app)

load_dotenv()


def token_user_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split()[1]  # Extract the JWT token from the header

        if not token:
            return 'Missing token', 401

        try:

            decoded = jwt.decode(token, algorithms="HS256",key= Config.JWT_SECRET_KEY)
            g.user_id = decoded['user_id']

        except jwt.ExpiredSignatureError:
            return 'Token expired', 401

        except jwt.InvalidTokenError:
            return 'Invalid token', 401

        except Exception as e:
            print(f"error: {e}")
            return jsonify({'message': 'Token is invalid!'}), 401

        return await f(*args, **kwargs)

    return decorated



def token_webhook_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split()[1]  # Extract the JWT token from the header

        if not token:
            return 'Missing token', 401

        try:
            decoded = jwt.decode(token, algorithms="HS256",key= Config.JWT_SECRET_KEY)
            g.page_id = decoded['page_id'] 
        except jwt.ExpiredSignatureError:
            return 'Token expired', 401

        except jwt.InvalidTokenError:
            return 'Invalid token', 401

        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return await f(*args, **kwargs)

    return decorated

@app.route('/send_message', methods=['POST'])
@token_webhook_required
async def webhook_send_message():
    page_id = g.page_id
    request_body = await request.get_json()
    
    text= request_body['text']
    user_id =request_body['user_id']
    print(text, user_id)
    try:
        page = await db.find_one_document("pages", {'page_id': page_id})
        if not page:
          return
        
        access_token = page['access_token']        

        send_message(recipient_id=user_id, page_id=page_id, text=text,access_token=access_token)
        return jsonify({"ok: true"}), 200
    except Exception as e:
        print(f"error: {e}") 
        return jsonify({'error': str(e)}), 500

@app.route("/add_page_info", methods=['POST'])
@token_user_required
async def set_page_info():
    user_id = g.user_id 
    request_body = await request.get_json()
    body = json.loads( request_body["body"])
    PAGE_ACCESS_TOKEN = body['page_access_token']
    PAGE_ID = body['page_id']
    try:
        response = await subscribe_app(PAGE_ID=PAGE_ID, PAGE_ACCESS_TOKEN=PAGE_ACCESS_TOKEN)
        if not  response:
            return jsonify({"error": "Failed to install app"}), 400
        
        result = await db.find_one_and_update("pages", {'page_id': PAGE_ID} ,{'$set':{
                'page_id': PAGE_ID,
                'user_id': user_id,
                'access_token': PAGE_ACCESS_TOKEN,
                'webhook': ''
            }}, upsert=True, new=True)
        if not result:
            return jsonify({"message": "Page_id not found"}), 404
        
        return jsonify({"message": "Page info added successfully."}), 200
    except Exception as e: 
        print(f"error: {e}")
        return jsonify({"error":str(e)}), 500

@app.route("/webhook", methods=['GET', 'POST'])
async def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    try: 
        if request.method == 'GET':
            return verify_webhook(request)

        if request.method == 'POST':
            signature = request.headers.get('X-Hub-Signature')
            data = await request.get_data()
            if not verify_signature(signature, data):
                return jsonify({"error": "Unsupported request method."}), 400
            
            payload = await  request.get_json()
            for entry in payload['entry']:
                page_id = entry['id']
                for event in entry['messaging']:
                    if is_user_message(event):
                        text = event['message']['text']
                        sender_id = event['sender']['id']
                        await handle_facebook_message(sender_id,page_id, text )

        return jsonify({'ok':True}),200
    except Exception as e:
        print(f"error: {e}")
        return jsonify({'ok':False}),500

@app.route('/set_webhook_url', methods=['POST'])
@token_user_required
async def set_webhook_url():
    request_body = await request.get_json()
    body = json.loads( request_body["body"])
    page_webhook_url = body["page_webhook_url"].strip()
    page_id = body["page_id"].strip()
    location = body["location"]
    field = body["field"]
    shop_link = body["shop_link"]
    
    if not has_valid_ssl(page_webhook_url):
       return jsonify({"error": "Insecure request. Please use HTTPS."}), 400
    
    document = await db.find_one_and_update("pages",{'page_id': page_id}, {'$set': {"webhook": page_webhook_url, "location": location, "field": field, "shop_link": shop_link}}, upsert=False, new=True)
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
    request_body = await request.get_json()

    access_token = request_body['access_token']
   
    try:
        response= await get_facebook_user(access_token=access_token)
        user_id = response['id']
        name = response['name']
        data =  await db.find_one_and_update("clients",{"client_id": user_id}, {"$set": {"client_id": user_id, "name": name}}, upsert=True, new = True)
        if data: 
            token = jwt.encode(
                    {'user_id': user_id, 'name': name},
                    Config.JWT_SECRET_KEY,
                    algorithm='HS256'
                )
            return jsonify({'token': token}), 200
        return jsonify({'message': 'Authentication failed'}), 401
    except Exception as e:
        print(f"error: {e}")
        return jsonify({'message': 'Authentication failed'}), 401

if __name__ == "__main__":
    app.run()
