from bson.objectid import ObjectId
from datetime import datetime, timedelta
from flask_jwt_extended import get_jwt_identity


class User:
    def __init__(self, fb_id, fb_name, name, phone_number, address):
        self.fb_id = fb_id
        self.fb_name = fb_name
        self.name = name
        self.phone_number = phone_number
        self.address = address

class Client:
    def __init__(self, username ,password,name):
        self.username = username
        self.password = password
        self.name = name

    def generate_access_token(self):
        from . import jwt
        return jwt.encode({
            'sub': str(self.id),
            'name': self.name,
            'exp': datetime.utcnow() + timedelta(seconds=3600)
        })

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'name': self.name
        }

    @staticmethod
    def get_user():
        identity = get_jwt_identity()
        if identity:
            return Client.objects(id=identity).first()

class Message:
    def __init__(self, message_id, user_id, text):
        self.message_id = message_id
        self.text = text
        self.user_id = user_id

class classifyReq:
    def __init__(self, _id, req, case, embedding):
        self._id = _id
        self.req = req
        self.case = case
        self.embedding = embedding
