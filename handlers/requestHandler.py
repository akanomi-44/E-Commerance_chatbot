from handlers.facebookHandler import send_message
from .chatgptHandler import get_gpt3_response

def applyFunction(func, text):
    return func(text)

def handle_case1(message):
    return get_gpt3_response(message)

def handle_case2(sender_id,message):
    isSuccess = False
    confirmation_message = '''
    Please fill in the following information:
    Product ID:
    Quantity:
    ''' 
    send_message(sender_id,confirmation_message) 
    
    #TODO: Add flow
     
    if isSuccess:
        return "Your order is registered."
    else: 
        return "There's an error occurred"

def handle_case3(message):
    return "Someone will contact with you shortly"
