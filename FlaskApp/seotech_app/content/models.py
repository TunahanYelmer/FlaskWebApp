from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import InputRequired, EqualTo, ValidationError, Email
import datetime
from seotech_app.database.database import init_db


def get_mongo(app):
    mongo = init_db(app)
    return mongo


class Customer:
    def __init__(self, name, email, subject, message, mongo):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message
        self.mongo = mongo

    def save(self):
        customer_collection = self.mongo.customer
        customer_data = {
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message,
            "dateOfRegister": datetime.datetime.utcnow(),
        }
        customer_collection.insert_one(customer_data)


class NewsLetter:
    def __init__(self, email, mongo):
        self.email = email
        self.mongo = mongo

    def save(self):
        newsletter_collection = self.mongo.newsfeed
        newsletter_data = {
            "email": self.email,
            "dateOfRegister": datetime.datetime.utcnow(),
        }
        newsletter_collection.insert_one(newsletter_data)


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
            "quote_link": self.quote_link,
            "image": self.image,
        }
        slider_collection.insert_one(slider_data)

    def retrive(self):
        slider_collection = self.mongo.slider

        slider_collection.find_one()


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

    def retrive(self):
        about_collection = self.mongo.about

        about_collection.find()


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

    def retrieve(self):
        service_collection = self.mongo.service

        service_collection.find()


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

    def retrieve(self):
        work_collection = self.mongo.work

        work_collection.find()


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
        self.link_yt = link_insta
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
            "link_yt": self.link_yt,
        }
        team_collection.insert_one(team_data)

    def retrive(self):
        team_collection = self.mongo.team
        team_collection.find()


class Client:
    def __init__(self, name, description, image, mongo):
        self.name = name
        self.description = description
        self.image = image
        self.mongo = mongo

    def save(self):
        client_collection = self.mongo.client
        client_data = {
            "name": self.name,
            "description": self.description,
            "image": self.image,
        }
        client_collection.insert_one(client_data)

    def retrive(self):
        client_collection = self.mongo.client
        client_collection.find()


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

    def retrive(self):
        contact_collection = self.mongo.contact

        contact_collection.find()


class Footer:
    def __init__(self, link_facebook, link_twitter, link_linkedin, link_youtube, mongo):
        self.link_facebook = link_facebook
        self.link_twitter = (link_twitter,)
        self.link_linkedin = link_linkedin
        self.link_youtube = link_youtube
        self.mongo = mongo

    def save(self):
        footer_collection = self.mongo.footer
        footer_data = {
            "facebook": self.link_facebook,
            "twitter": self.link_twitter,
            "linkedin": self.link_linkedin,
            "youtube": self.link_youtube,
        }
        footer_collection.insert_one(footer_data)

    def retrive(self):
        footer_collection = self.mongo.footer
        footer_data = {
            "facebook": self.link_facebook,
            "twitter": self.link_twitter,
            "linkedin": self.link_linkedin,
            "youtube": self.link_youtube,
        }
        footer_collection.find_one(footer_data)


class CustomerMessageForm(FlaskForm):
    form_name = HiddenField("form_name")
    name = StringField("Name", [InputRequired()], render_kw={"placeholder": "Name","class":"form-control"})
    email = StringField("Email", [InputRequired(), Email()], render_kw={"placeholder": "Email","class":"form-control"})
    subject = StringField("Subject", [], render_kw={"placeholder": "Subject","class":"form-control"})
    message = StringField("Message", [InputRequired()], render_kw={"placeholder": "Message","class":"form-control"})


class NewsLetterForm(FlaskForm):
    form_name = HiddenField("form_name")
    email = StringField(
        "Email", [InputRequired(), Email()], render_kw={"placeholder": "Email"}
    )
