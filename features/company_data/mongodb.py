import os
from pymongo import MongoClient
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

ENV_FILE = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_FILE)

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
db = client["worksphere"]
companies = db["companies"]
reviews = db["reviews"]
job_roles = db["job_roles"]
def test_connection():
    client.admin.command("ping")
    print("MongoDB connection successful!")