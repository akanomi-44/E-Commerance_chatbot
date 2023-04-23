from db.mongo import db
from db.models import *
from db.schema import *

def create_user(user_data):
    # Deserialize request JSON to User object
    user = User(**user_data)

    # Insert User object into database
    result = db.users.insert_one(user.__dict__)

    # Get inserted User object from database
    inserted_user = db.users.find_one({'_id': result.inserted_id})

    # Serialize User object to response JSON using UserSchema
    user_schema = UserSchema()
    response_data = user_schema.dump(inserted_user)

    return response_data


def get_user(user_data):

    print(user_data)
    # Deserialize request JSON to User object
    user = User(**user_data)

    print(user)
    # Get inserted User object from database
    inserted_user = db.users.find_one(user)

    # Serialize User object to response JSON using UserSchema
    user_schema = UserSchema()
    response_data = user_schema.dump(inserted_user)

    return response_data
