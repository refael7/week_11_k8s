import os
from bson import ObjectId
from pymongo import  MongoClient
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

    def __repr__(self):
        return f"Contact(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, phone_number={self.phone_number})"

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

def create_contact(contact_data: dict)-> str | None:
    conn = get_connection()
    if conn is None:
        return  None
    db = conn["MONGO_DB"]
    contacts_collection = db["contacts"]
    result = contacts_collection.insert_one(contact_data)
    return str(result.inserted_id)

def get_all_contacts() -> list[Contact] | None:
    conn = get_connection()
    if conn is None:
        return None

    db = conn[os.environ["MONGO_DB"]]
    contacts_collection = db["contacts"]
    contacts_cursor = contacts_collection.find()
    contacts = []

    for contact_data in contacts_cursor:
        contact = Contact(
            id=str(contact_data["_id"]),
            first_name=contact_data["first_name"],
            last_name=contact_data["last_name"],
            phone_number=contact_data["phone_number"]
        )
        contacts.append(contact)

    return contacts



def update_contact(id: str, contact_data: dict) -> bool | None:
    conn = get_connection()
    if conn is None:
        return None

    db = conn[os.environ["MONGO_DB"]]
    contacts_collection = db["contacts"]
    object_id = ObjectId(id)

    result = contacts_collection.update_one(
        {"_id": object_id},
        {"$set": contact_data}
    )

    return result.modified_count > 0


def delete_contact(id: str) -> bool| None:

    conn = get_connection()
    if conn is None:
        return None
    db = conn[os.environ["MONGO_DB"]]
    contacts_collection = db["MONGO_COLLECTION"]
    result = contacts_collection.delete_one({"id": id})
    return result.deleted_count > 0