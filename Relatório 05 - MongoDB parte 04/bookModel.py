from pymongo import MongoClient
from bson.objectid import ObjectId

class BookModel:
    def __init__(self, database):
        self.db = database

    def create_book(self, title:str, autor: str, year: int, price: float):
        try:
            res = self.db.collection.insert_one({"title": title, "autor": autor, "year": year, "price": price})
            print(f"Book created with id: {res.inserted_id}")
            return res.inserted_id
        except Exception as e:
            print(f"An error occurred while creating book: {e}")
            return None

    def read_book_by_id(self, id: str):
        try:
            res = self.db.collection.find_one({"_id": ObjectId(id)})
            print(f"Book found: {res}")
            return res
        except Exception as e:
            print(f"An error occurred while reading book: {e}")
            return None

    def update_book(self, id: str, title:str, autor: str, year: int, price: float):
        try:
            res = self.db.collection.update_one({"_id": ObjectId(id)}, {"$set": {"title": title, "autor": autor, "year": year, "price": price}})
            print(f"Book updated: {res.modified_count} document(s) modified")
            return res.modified_count
        except Exception as e:
            print(f"An error occurred while updating book: {e}")
            return None

    def delete_book(self, id: str):
        try:
            res = self.db.collection.delete_one({"_id": ObjectId(id)})
            print(f"Book deleted: {res.deleted_count} document(s) deleted")
            return res.deleted_count
        except Exception as e:
            print(f"An error occurred while deleting book: {e}")
            return None
        
    