from db.mongo import db
from db.models import *
from db.schema import *

def get_cloth(cloth_data):

    print(cloth_data)
    # Deserialize request JSON to Clothes object
    cloth = Clothes(**cloth_data)

    print(cloth)
    # Get inserted User object from database
    inserted_cloth = db.cloths.find_one(cloth)

    # Serialize User object to response JSON using ClothesSchema
    cloth_schema = ClothesSchema()
    response_data = cloth_schema.dump(inserted_cloth)

    return response_data
