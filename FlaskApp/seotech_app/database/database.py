# seotech_app/database/database.py
from flask import Flask 
from pymongo import MongoClient


def init_db(app):
    # Explicitly retrieve the MongoDB URI from the app config
    mongo_uri = app.config.get("MONGO_URI")
    client=MongoClient(mongo_uri)
    mongo=client.SeoTechDatabase
    if not mongo_uri:
        raise ValueError("MONGO_URI is not set in the Flask app config.")
    # Explicitly pass the MongoDB URI to PyMongo
    return mongo
