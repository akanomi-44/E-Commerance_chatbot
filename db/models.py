from mongoengine import Document, StringField


class User(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    fb_id = StringField(required=True, unique = True)
    phone_number = StringField()
    address = StringField()

class Client(Document):
    username = StringField(required= True)
    password = StringField(required= True)
    access_token = StringField(required= True)

class Message(Document):
    message_id = StringField(required= True)
    text = StringField(required= True)
    user_id = StringField(required= True)
    page_id = StringField(required= True)

class Page(Document):
    page_id = StringField(required= True)
    access_token = StringField(required= True)
    client_id = StringField(required=True)

class classifyReq:
    def __init__(self, _id, req, case, embedding):
        self._id = _id
        self.req = req
        self.case = case
        self.embedding = embedding
