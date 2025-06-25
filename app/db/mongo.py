from pymongo import MongoClient
from app.config import MONGO_URI, MONGO_DB_NAME

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]

logs_collection = mongo_db["agent_logs"]
system_info_collection = mongo_db["system_info"]
