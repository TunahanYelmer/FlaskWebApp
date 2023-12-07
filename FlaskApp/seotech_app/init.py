from flask import Flask
from flask_pymongo import PyMongo
import os 

app =Flask(__name__)
app.config['MONGO_URI']='mongodb+srv://tunahanyelmer:<TunaYel.41>@cluster0.zwojfzw.mongodb.net/?retryWrites=true&w=majority'
db = PyMongo(app)

from seotech_app.frontend.views import main
app.register_blueprint(main)
def check_connection():
    return db.cx.server_info()  # This will throw an exception if it cannot connect to the MongoDB server

if __name__ == "__main__":
    print(check_connection())  # Print server info to check connection
    app.run(debug=True)

