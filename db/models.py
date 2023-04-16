from bson.objectid import ObjectId

class User:
    def __init__(self, fb_id, fb_name, name, phone_number, address):
        self.fb_id = fb_id
        self.fb_name = fb_name
        self.name = name
        self.phone_number = phone_number
        self.address = address

class Clothes:
    def __init__(self, name, brand, description, variants):
        self.name = name
        self.brand = brand
        self.description = description
        self.variants = variants

class Bill:
    def __init__(self, user_id, clothes_ids, shipping_address):
        self.user_id = user_id
        self.clothes_ids = clothes_ids
        self.shipping_address = shipping_address

class Transaction:
    def __init__(self, bill_id, total_amount):
        self.bill_id = bill_id
        self.total_amount = total_amount
