from db.mongo import db
from db.models import *
from db.schema import *

def create_transaction(transaction_data):
    # Deserialize request JSON to Transaction object
    transaction = Transaction(**transaction_data)

    # Insert Transaction object into database
    result = db.transactions.insert_one(transaction.__dict__)

    # Get inserted Transaction object from database
    inserted_transaction = db.transactions.find_one({'_id': result.inserted_id})

    # Serialize Transaction object to response JSON using TransactionSchema
    transaction_schema = TransactionSchema()
    response_data = transaction_schema.dump(inserted_transaction)

    return response_data
