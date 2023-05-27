import httpx
from .chatgptHandler import get_gpt3_response

def handle_case1(message):
    prompt = f"{message}. Return result as a list"
    return get_gpt3_response(prompt)

def handle_case2(message):
    return f"You can make an order here: <e-com platform links>"

def handle_case3(message):
    return "I have notified Store Owner. In the meantime if you have any questions please let me know"
    
def handle_case4(location):
    if location != "":
        return f"Our shop is located at {location}"
    else:
        return f"We don't have an official location yet, but we're working on it. Stay tuned for updates on our website and social media. Thank you for your interest!"

def handle_default(message, field):
    prompt = f"User: {message}. Give me a response if related to {field} else answer only 'No'"
    message = get_gpt3_response(prompt)
    if message != "No":
        return message
    else:
        return f"I can only process request that is in following cases:\n\n 1. Recommendation: Can you recommend some [product] for [event] ?,...  \n\n 2. Make an order: Where can i order this [item],... \n\n 3. Contact human assistant: Contact the manager,... \n\n 4. Answer related questions: What is the fashion trend of the 90s ?,... ?"

async def send_webhook_message( type, message, user_id, url):
    payload = {
        "user_id": user_id,
        "type":type,
        "message": message
    }
    headers = {
            'Content-Type': 'application/json'
        }
    
    async with httpx.AsyncClient() as client:
        response= await client.post(url, headers=headers,json=payload)
        return response.json()
    # async with httpx.AsyncClient() as client:
    #     async with session.post(url, json=payload, headers=headers) as response:
    #         result = await response.json()
    #         return result