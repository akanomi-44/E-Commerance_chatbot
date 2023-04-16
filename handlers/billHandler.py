from db.mongo import db
from db.models import *
from db.schema import *

def create_bill(bill_data):
    # Deserialize request JSON to Bill object
    bill = Bill(**bill_data)

    # Insert Bill object into database
    result = db.bills.insert_one(bill.__dict__)

    # Get inserted Bill object from database
    inserted_bill = db.bills.find_one({'_id': result.inserted_id})

    # Serialize Bill object to response JSON using BillSchema
    bill_schema = BillSchema()
    response_data = bill_schema.dump(inserted_bill)

    return response_data


def get_bill(bill_data):

    print(bill_data)
    # Deserialize request JSON to Bill object
    bill = Bill(**bill_data)

    print(bill)
    # Get inserted Bill object from database
    inserted_bill = db.bills.find_one(bill)

    # Serialize Bill object to response JSON using BillSchema
    bill_schema = BillSchema()
    response_data = bill_schema.dump(inserted_bill)

    return response_data
