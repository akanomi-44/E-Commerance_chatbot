from .chatgptHandler import get_gpt3_response, check_relativity

def handle_case1(message):
    prompt = f"{message}. Return result as a list"
    return get_gpt3_response(prompt)

def handle_case2(message):
    return f"You can make an order here: <e-com platform links>"

def handle_case3(message):
    return "Someone will contact with you shortly"
    
def handle_default(message):
    is_related = check_relativity(message)
    if is_related == "Y":
        return get_gpt3_response(message)
    else:
        return "Sorry! your request can not be processed"