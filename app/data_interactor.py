import os
from pymongo import AsyncMongoClient, MongoClient
from dotenv import load_dotenv
load_dotenv()
class Contact:
    def __init__(self, id:int, first_name:str, last_name:str, phone_number:str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def convert_contact_to_dictionary(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number
        }

def get_connection():
    try:
        conn = MongoClient(
            host=os.environ["MONGO_HOST"],
            port=int(os.environ["MONGO_PORT"])
        )
        conn.admin.command("ping")
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

