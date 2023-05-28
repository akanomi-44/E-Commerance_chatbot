import httpx
from .chatgptHandler import get_gpt3_response

def handle_case1(message):
    prompt = f"{message}. Return result as a list"
    return get_gpt3_response(prompt)

def handle_case2(shop_link):
    return f"You can make an order here: {shop_link}"

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
    if message not in  ["No", "No."]:
        return message
    else:
        return f"I can only process request that is in following cases:\n\n 1. Recommendation: Can you recommend some [product] for [event] ?,...  \n\n 2. Make an order: Where can i order this [item],... \n\n 3. Contact human assistant: Contact the manager,... \n\n 4. Answer related questions: What is the fashion trend of the 90s ?,How do I properly care for and store my leather jackets ?,...  \n\n 5. Get shop's location: Where can i find your shop,..."

async def send_webhook_message(type, message, user_id, url):
    payload = {
        "user_id": user_id,
        "type": type,
        "message": message
    }
    headers = {
        'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                print("Success: Request was successful.")
                return response.json()

            elif response.status_code == 400:
                print("Bad Request: The server could not process the request.")

            elif response.status_code == 404:
                print("Not Found: The requested resource was not found.")

            elif response.status_code == 500:
                print("Internal Server Error: An error occurred on the server.")
            else:
                print(f"Unexpected Status Code: {response.status_code}")

            return   
        except httpx.RequestError as exc:
            print(f"An error occurred while sending the webhook: {exc}")
            return