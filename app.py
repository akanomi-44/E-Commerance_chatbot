from flask import Flask, request, jsonify
import requests
from config import Config
from db.mongo import pagesCollection
from dotenv import load_dotenv

from handlers.facebookHandler import handle_facebook_message, is_user_message, verify_signature, verify_webhook
from handlers.sslHandler import has_valid_ssl
app = Flask(__name__)

load_dotenv()



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
            'app_id': Config.APP_ID,
            'subscribed_fields': 'messages',
            'access_token': PAGE_ACCESS_TOKEN 
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            result = pagesCollection.find_one({'page_id': PAGE_ID})
        

            print(result)
            if result is None:
                pagesCollection.insert_one({
                    'page_id': PAGE_ID,
                    'user_id': user_id,
                    'access_token': PAGE_ACCESS_TOKEN,
                    'webhook': ''
                })
            else:
                pagesCollection.update_one({'page_id': PAGE_ID}, {'$set': {'access_token': PAGE_ACCESS_TOKEN}})
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
                    page = pagesCollection.find_one({'page_id': page_id})
                    if page:
                        handle_facebook_message(sender_id,page_id, text )

        return "ok"

@app.route('/set_webhook_url', methods=['POST'])
def set_webhook_url():
    page_webhook_url = request.json.get("page_webhook_url")
    page_id = request.json.get("page_id")
    if not has_valid_ssl(page_webhook_url):
       return jsonify({"error": "Insecure request. Please use HTTPS."}), 400
    
    query = {'page_id': page_id}
    document = pagesCollection.find_one(query)
    if document:
        document['webhook'] = page_webhook_url
        pagesCollection.update_one(query, {'$set': document})
    else: 
        return jsonify({"error": "Page Id not exist in database."}), 400
    
    return jsonify({"message": "Add successfully."}), 200
    
@app.route('/getWebhooks', methods=['GET'])
def getWebhooks():
    user_id = request.args.get('user_id')

    query = {'user_id': user_id}
    document = pagesCollection.find(query)
    if document: 
        return jsonify(document), 200
    
    return jsonify({"error": "user_id not exist in database."}), 400
    

def main():
    app.run()


if __name__ == "__main__":
    main()