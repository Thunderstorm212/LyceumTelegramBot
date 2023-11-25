from pymongo.mongo_client import MongoClient
from conf import DB_TOKEN, DB_USER


cluster = "cluster0"
uri = f"mongodb+srv://{DB_USER}:{DB_TOKEN}@{cluster}.gbcrwrb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
customer_db = client["customer"]
users_collection = customer_db["users"]

print("Db status is", customer_db.command('ping'))
