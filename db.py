import os
from urllib.parse import urlparse
import pymongo
from pymongo import MongoClient

USERNAME = "user0"
PASSWORD = "5gdGDHiTfYz0fKD2"
DATABASE_NAME = "crescorex"
DATABASE_URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0-nzzqi.mongodb.net/{DATABASE_NAME}?retryWrites=true&w=majority"

""" experimental code segment """
COLLECTIONS = {
    "otp": ("code", "uid", "expire_time"),
    "customer": ("phone", "credit_score"),
    "user": (
        "full_name",
        "password",
        "birth_day",
        "bank_id",
        "branch_id",
        "uid",
        "phone",
        "search_history",
        "email",
        "role",
    ),
    "loan": (
        "loan_id",
        "bank_id",
        "branch_id",
        "customer_phone_number",
        "amount",
        "type",
        "tenor",
        "status",
    ),
    "bank": (
        "bank_id",
        "bank_name",
        "license_key",
        "branch",
        "branch_id",
        "staff_list",
        "expire_date",
    ),
}
""" END experimental code segment """

if __name__ == "__main__":
    """
    for debugging purpose
    """

    client: pymongo.mongo_client.MongoClient = MongoClient(DATABASE_URI)

    db: pymongo.database.Database = client[DATABASE_NAME]

    print(DATABASE_URI)
    print(type(db))
    print(db)
