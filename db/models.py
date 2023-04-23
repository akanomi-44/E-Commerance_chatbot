from bson.objectid import ObjectId

class User:
    def __init__(self, fb_id, fb_name, name, phone_number, address):
        self.fb_id = fb_id
        self.fb_name = fb_name
        self.name = name
        self.phone_number = phone_number
        self.address = address

class Message:
    def __init__(self, message_id, user_id, text):
        self.message_id = message_id
        self.text = text
        self.user_id = user_id
