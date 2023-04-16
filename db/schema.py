from marshmallow import Schema, fields

class UserSchema(Schema):
    fb_id = fields.String()
    fb_name = fields.String()
    name = fields.String()
    phone_number = fields.String()
    address = fields.String()

class ClothesVariantSchema(Schema):
    size = fields.String()
    color = fields.String()
    price = fields.Float()

class ClothesSchema(Schema):
    name = fields.String()
    brand = fields.String()
    description = fields.String()
    variants = fields.List(fields.Nested(ClothesVariantSchema))

class BillSchema(Schema):
    user_id = fields.String()
    clothes_ids = fields.List(fields.String())
    shipping_address = fields.String()
    billing_date = fields.DateTime()
    billing_amount = fields.Float()

class TransactionSchema(Schema):
    bill_id = fields.String()
    total_amount = fields.Float()

class MessageSchema(Schema):
    message_id = fields.String()
    user_id = fields.String()
    text = fields.String()
