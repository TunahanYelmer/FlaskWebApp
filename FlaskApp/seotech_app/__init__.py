from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin, BaseView, expose
from flask_toastr import Toastr


from pathlib import Path
from seotech_app.content import models
import os

# seotech_app/__init__.py


def create_app():
    app = Flask(__name__)

    # Add your database configuration here if needed
    # Example: app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'

    # Import and configure extensions
    toast=Toastr(app)
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)
    # Load sensitive information from environment variables
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
    app.config["SECRET_KEY"] = "your_secret_key_here"
    
    # Check if the MongoDB URI is properly configured
    if app.config["MONGO_URI"] is None:
        raise ValueError("MONGO_URI is not set in the environment variables.")

    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    from seotech_app.content import main
    from seotech_app.admin import admin_

    app.register_blueprint(main)

    app.register_blueprint(admin_)

    # Import and register blueprints

    # Register other blueprints if needed

    # Import and register models (assuming you have models in content package)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app
