from marshmallow import Schema, fields

class UserSchema(Schema):
    fb_id = fields.String()
    fb_name = fields.String()
    name = fields.String()
    phone_number = fields.String()
    address = fields.String()

class MessageSchema(Schema):
    message_id = fields.String()
    user_id = fields.String()
    text = fields.String()

class ClassifyReqSchema(Schema):
    _id = fields.UUID()
    req = fields.String()
    case = fields.String()
    embedding = fields.List()