from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    TextAreaField,
    SubmitField,
)
from wtforms.validators import InputRequired, EqualTo, ValidationError, Email
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from seotech_app.database.database import init_db


def get_mongo(app):
    mongo = init_db(app)
    return mongo


def InputMustBeEqual(form, field):
    if field.data != form.password.data:
        raise ValidationError("Passwords must match")


class User:
    def __init__(self, username, password, email, name, is_admin, mongo):
        self.username = username
        self.passwrdhash = password
        self.email = email
        self.name = name
        self.is_admin = is_admin
        self.mongo = mongo

    def save(self):
        user_collection = self.mongo.users
        user_data = {
            "email": self.email,
            "passwrdHash": self.passwrdhash,
            "dateOfRegister": datetime.datetime.utcnow(),
            "is_Admin": self.is_admin,
            "name": self.name,
            "username": self.username,
        }
        user_collection.insert_one(user_data)


class Slider:
    def __init__(self, title, contact_link, quote_link, description, image, mongo):
        self.title = title
        self.description = description
        self.contact_link = contact_link
        self.quote_link = quote_link
        self.image = image
        self.mongo = mongo

    def save(self):
        slider_collection = self.mongo.slider
        slider_data = {
            "title": self.title,
            "description": self.description,
            "contact_link": self.contact_link,
            "image": self.image,
            "quote_link": self.quote_link,
        }
        slider_collection.insert_one(slider_data)


class About:
    def __init__(self, title, description, read, image, mongo):
        self.title = title
        self.description = description
        self.image = image
        self.read = read
        self.mongo = mongo

    def save(self):
        about_collection = self.mongo.about
        about_data = {
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "read": self.read,
            
        }
        about_collection.insert_one(about_data)


class Service:
    def __init__(
        self, title, description, service_title, service_description, read, image, mongo
    ):
        self.title = title
        self.description = description
        self.service_title = service_title
        self.service_description = service_description
        self.read = read
        self.image = image
        self.mongo = mongo

    def save(self):
        service_collection = self.mongo.service
        service_data = {
            "title": self.title,
            "description": self.description,
            "service_title": self.service_title,
            "service_description": self.service_description,
            "read": self.read,
            "image": self.image,
        }
        service_collection.insert_one(service_data)


class Work:
    def __init__(
        self, title, description, service_title, service_description, read, image, mongo
    ):
        self.title = title
        self.description = description
        self.service_title = service_title
        self.service_description = service_description
        self.read = read
        self.image = image
        self.mongo = mongo

    def save(self):
        work_collection = self.mongo.work
        work_data = {
            "title": self.title,
            "description": self.description,
            "service_title": self.service_title,
            "service_description": self.service_description,
            "read": self.read,
            "image": self.image,
        }
        work_collection.insert_one(work_data)


class Team:
    def __init__(
        self,
        name,
        description,
        image,
        link_fb,
        link_tw,
        link_linkedin,
        link_insta,
        mongo,
    ):
        self.name = name
        self.description = description
        self.image = image
        self.link_fb = link_fb
        self.link_tw = link_tw
        self.link_linkedin = link_linkedin
        self.link_insta = link_insta
        self.mongo = mongo

    def save(self):
        team_collection = self.mongo.team
        team_data = {
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "link_fb": self.link_fb,
            "link_tw": self.link_tw,
            "link_linkedin": self.link_linkedin,
            "link_insta": self.link_insta,
        }
        team_collection.insert_one(team_data)


class Clients:
    def __init__(self, title, description, client_title, client_description, read, image, mongo):
        self.title = title
        self.description = description
        self.client_title = client_title
        self.client_description = client_description
        self.read = read
        self.image = image
        self.mongo = mongo

    def save(self):
            clients_collection = self.mongo.clients
            clients_data = {
                "title": self.title,
                "description": self.description,
                "client_title": self.client_title,
                "client_description": self.client_description,
                "read": self.read,
                "image": self.image,
            }
            clients_collection.insert_one(clients_data)


class Contact:
    def __init__(self, telephone, email, mongo):
        self.telephone = telephone
        self.email = email
        self.mongo = mongo

    def save(self):
        contact_collection = self.mongo.contact
        contact_data = {
            "telephone": self.telephone,
            "email": self.email,
        }
        contact_collection.insert_one(contact_data)


class Footer:
    def __init__(
        self,
        title,
        description,
        link_facebook,
        link_twitter,
        link_linkedin,
        link_youtube,
        mongo,
    ):
        self.title = title
        self.description = description
        self.link_facebook = link_facebook
        self.link_twitter = (link_twitter,)
        self.link_linkedin = link_linkedin
        self.link_youtube = link_youtube
        self.mongo = mongo

    def save(self):
        footer_collection = self.mongo.footer
        footer_data = {
            "title": self.title,
            "description": self.description,
            "link_facebook": self.link_facebook,
            "link_twitter": self.link_twitter,
            "link_linkedin": self.link_linkedin,
            "link_youtube": self.link_youtube,
        }
        footer_collection.insert_one(footer_data)


class RegistrationForm(FlaskForm):
    email = StringField("Email", [InputRequired(), Email()])
    username = StringField("Username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    name = StringField("Name", [InputRequired()])
    confirm = PasswordField("Confirm Password", [InputRequired(), InputMustBeEqual])


class LoginForm(FlaskForm):
    username = StringField("Username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])


class AdminUserCreateForm(FlaskForm):
    username = StringField("Username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    admin = BooleanField("Is Admin?")


class AdminUserUpdateForm(FlaskForm):
    email = StringField("Email", [InputRequired(), Email()])
    username = StringField("Username", [InputRequired()])
    name = StringField("Name", [InputRequired()])
    admin = BooleanField("Is Admin?")


class AdminSendEmailForm(FlaskForm):
    email = StringField("Email", [Email()])
    subject = StringField("Subject", [InputRequired()])
    message = TextAreaField("Message", [InputRequired()])


class AdminEditSliderForm(FlaskForm):
    title = StringField("Title", [InputRequired()])
    contact_link = StringField("Contact Link", [InputRequired()])
    quote_link = StringField("Quote Link", [InputRequired()])
    description = TextAreaField("Description", [InputRequired()])
    image = FileField("Image", [FileAllowed(["jpg", "png", "jpeg"])])


class AdminEditAboutForm(FlaskForm):
    title = StringField("Title", [InputRequired()])
    description = TextAreaField("Description", [InputRequired()])
    read = StringField("Read More Link", [InputRequired()])
    image = FileField("Image", [FileAllowed(["jpg", "png", "jpeg"])])


class AdminEditServiceForm(FlaskForm):
    title = StringField("Title", [InputRequired()])
    description = TextAreaField("Description", [InputRequired()])
    service_title = StringField("Service Title", [InputRequired()])
    service_description = TextAreaField("Service Description", [InputRequired()])
    read = StringField("Read More Link", [InputRequired()])
    image = FileField("Image", [FileAllowed(["jpg", "png", "jpeg"])])


class AdminEditWorkForm(AdminEditServiceForm):
    title = StringField("Title", [InputRequired()])
    description = TextAreaField("Description", [InputRequired()])
    service_title = StringField("Service Title", [InputRequired()])
    service_description = TextAreaField("Service Description", [InputRequired()])
    read = StringField("Read More Link", [InputRequired()])
    image = FileField("Image", [FileAllowed(["jpg", "png", "jpeg"])])


class AdminEditTeamForm(FlaskForm):
    name = StringField("Name", [InputRequired()])
    description = TextAreaField("Description", [InputRequired()])
    image = FileField("Image", [FileAllowed(["jpg", "png", "jpeg"])])
    link_fb = StringField("Facebook Link")
    link_tw = StringField("Twitter Link")
    link_linkedin = StringField("LinkedIn Link")
    link_insta = StringField("Instagram Link")


class AdminEditClientForm(FlaskForm):
    title = StringField("Title", [InputRequired()])
    description = TextAreaField("Description", [InputRequired()])
    client_title = StringField("Client Title", [InputRequired()])
    client_description = TextAreaField("Service Description", [InputRequired()])
    read = StringField("Read More Link", [InputRequired()])
    image = FileField("Image", [FileAllowed(["jpg", "png", "jpeg"])])


class AdminEditContactForm(FlaskForm):
    telephone = StringField("Telephone", [InputRequired()])
    email = StringField("Email", [InputRequired(), Email()])


class AdminEditFooterForm(FlaskForm):
    title = StringField("Title", [InputRequired()])
    description = TextAreaField("Description", [InputRequired()])
    link_facebook = StringField("Facebook Link")
    link_twitter = StringField("Twitter Link")
    link_linkedin = StringField("LinkedIn Link")
    link_youtube = StringField("Youtube Link")
