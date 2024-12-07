from pymongo import MongoClient


def get_mongodb():
    client = MongoClient(
        "mongodb+srv://InvisUA:Pass321@cluster0.hqwgv.mongodb.net/mydatabase?retryWrites=true&w=majority&appName=Cluster0"
    )
    db = client.hw
    return db
