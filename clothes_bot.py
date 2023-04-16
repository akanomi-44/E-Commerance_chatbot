import openai
import re
import APIkey

from handlers.clothHandler import get_cloth
from db.mongo import db

# Set up a connection to the OpenAI API
openai.api_key = APIkey.get_key()

# Define a function to search for clothes in the database based on the given parameters
def search_clothes(name=None, color=None, size=None, quantity=None, price=None):
    query = {}
    if name:
        query['name'] = name
    if color:
        query['color'] = color
    if size:
        query['size'] = size
    if quantity:
        query['quantity'] = {'$gte': quantity}
    if price:
        query['price'] = {'$lte': price}
    return list(db.clothes.find(query))


# Define a function to send a message to the GPT-3 API and retrieve a response
def get_gpt3_response(message):
    prompt = "Please return name, color, size of clothes based on the customer's message (if the value does not exist, please return None):\nCustomer: " + message + "\nClothes:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )
    return response.choices[0].text


def extract_search_parameters(response):
    search_params = {}
    match = re.search('Name: (.*?), Color: (.*?), Size: (.*?).', response)
    if match:
        search_params['name'] = match.group(1).strip()
        search_params['color'] = match.group(2).strip()
        search_params['size'] = match.group(3).strip()
    return search_params


# Define a function to handle customer messages
def handle_message(message):
    # Send the message to the GPT-3 API and retrieve a response
    response = get_gpt3_response(message)
    
    print(response)

    # Extract search parameters from the GPT-3 response
    clothes = extract_search_parameters(response)
    
    name=clothes['name']
    if(name == 'None'):
        name = None
    color = clothes['color']
    if(color == 'None'):
        color = None
    size = clothes['size']
    if(size == 'None'):
        size = None

    # Search for clothes in the database based on the extracted search parameters
    results = search_clothes(name,color,size)

    # Present the search results to the customer
    if len(results) == 0:
        return "I'm sorry, I couldn't find any clothes that match your search criteria."
    else:
        result_strings = []
        for result in results:
            result_strings.append(f"{result['name']} in {result['color']} color, size {result['size']}, quantity {result['quantity']}, price {result['price']}")
        return "I found the following clothes that match your search criteria:\n" + "\n".join(result_strings)


# if __name__ == '__main__':
#     message = 'I want to buy a blue jeans.'
#     result = handle_message(message)
#     print(result)