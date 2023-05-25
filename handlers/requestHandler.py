from .chatgptHandler import get_gpt3_response
import requests

def handle_case1(message):
    prompt = f"{message}. Return result as a list"
    return get_gpt3_response(prompt)

def handle_case2(message):
    return f"You can make an order here: <e-com platform links>"

def handle_case3(message):
    return "Someone will contact with you shortly"
    
def handle_default(message, field):
    prompt = f"User: {message}. Give me a response with {field} suggestions or details if related else answer only 'No'"
    message = get_gpt3_response(prompt)
    if message != "No.":
        return message
    else:
        return f"I can only process request that is in following cases:\n\n 1. Recommendation: Can you recommend some clothes for [event] ?,...  \n\n 2. Make an order: Where can i order this [item],... \n\n 3. Contact human assistant: Contact the manager,... \n\n 4. Answer related questions: What is the fashion trend of the 90s ?,... ?"

def send_webhook_message(type, message, user_id, url):
    payload = {
        "user_id": user_id,
        "type":type,
        "message": message
    }
    headers = {
            'Content-Type': 'application/json'
        }
    try:
        requests.post(url=url, headers=headers, json=payload)
    except:
        print(url, "error")