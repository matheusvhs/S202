from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
db = client.delivery
pedidos_collection = db.pedidos
