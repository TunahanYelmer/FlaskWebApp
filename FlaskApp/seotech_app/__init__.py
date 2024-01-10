import 
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
import os

app = Flask(__name__)

# Load sensitive information from environment variables
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# Check if the MongoDB URI is properly configured
if app.config["MONGO_URI"] is None:
    raise ValueError("MONGO_URI is not set in the environment variables.")

db = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User loader function
from seotech_app.content.models import (
    User,
)  # Adjust the import based on your actual model


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Import blueprints
from seotech_app.content.views import main
from seotech_app.admin.admin_views import admin_

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(admin_)

if __name__ == "__main__":
    print(check_connection())  # Print server info to check connection
    app.run(debug=True)
