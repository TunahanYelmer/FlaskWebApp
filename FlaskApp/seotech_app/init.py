from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://tunahanyelmer:<TunaYel.41>@cluster0.zwojfzw.mongodb.net/?retryWrites=true&w=majority'
db = PyMongo(app)

def check_connection():
    return db.cx.server_info()

from seotech_app.frontend.views import main
app.register_blueprint(main)

if __name__ == "__main__":
    print(check_connection())  # Print server info to check connection
    app.run(debug=True)
