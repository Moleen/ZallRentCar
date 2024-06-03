from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


SECRET_KEY_DASHBOARD = os.environ.get("SECRET_KEY_DASHBOARD")
MONGODB_URI = os.environ.get("MONGODB_URI")
DB =  os.environ.get("DB")

def dataBase():
    client = MongoClient(MONGODB_URI)
    db = client[DB]
    return db
    

        