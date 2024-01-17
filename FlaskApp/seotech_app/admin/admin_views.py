from flask import (
    request,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    Blueprint,
    current_app as app,
    g,
)
from flask_login import current_user
from flask_admin import AdminIndexView

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from seotech_app.admin.admin_models import (
    User,
    RegistrationForm,
    LoginForm,
    AdminUserCreateForm,
    AdminUserUpdateForm,
    AdminSendEmailForm,
    AdminEditSliderForm,
    AdminEditAboutForm,
    AdminEditServiceForm,
    AdminEditTeamForm,
    AdminEditContactForm,
    AdminEditFooterForm,
    AdminEditClientForm,
    AdminEditWorkForm,
    Clients,
    Slider,
    About,
    Service,
    Team,
    Contact,
    Work,
    Footer,
)
import os
from pathlib import Path
from seotech_app.admin.admin_models import get_mongo
from dotenv import load_dotenv

from flask_admin import BaseView, expose
from flask import abort
from functools import wraps
from bson import ObjectId
from mailjet_rest import Client

admin_ = Blueprint("admin_", __name__)


@admin_.before_request
def before_request():
    g.user = current_user


def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not session.get("username"):
            flash({"message": "You Need To Login First"}, "Warning")
            return redirect(url_for("admin_.admin_login"))
        return func(*args, **kwargs)

    return decorated_view


@admin_.route("/admin/register", methods=["GET", "POST"])
def admin_register():
    mongo = get_mongo(app)
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        name = form.name.data
        user_collection = mongo.users
        existing_user = user_collection.find_one({"username": username})
        existing_email = user_collection.find_one({"email": email})
        print("Existing User:", existing_user)
        if existing_user:
            flash(
                {
                    "title": "Warning",
                    "message": "This username has been already taken. Try another one.",
                },
                "warning",
            )
            return render_template("admin_register.html", form=form)
        elif existing_email:
            flash(
                {
                    "title": "Warning",
                    "message": "This email has been already taken. Try another one.",
                },
                "warning",
            )
            return render_template("admin_register.html", form=form)
        else:
            passwrdhash = generate_password_hash(password)
            user = User(username, passwrdhash, email, name, False, mongo)
            user.save()
            flash(
                {"title": "Success", "message": "You are succesfully registered."},
                "success",
            )
            return redirect(url_for("admin_.admin_login"))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    {"title": "Error", "message": f"Error in {field}:{error}"},
                    "error",
                )
    return render_template("admin_register.html", form=form, user=current_user)


@admin_.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    mongo = get_mongo(app)
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_collection = mongo.users
        user = user_collection.find_one({"username": username})
        if user is None:
            flash("This username does not exist.", "info")
            return render_template("admin_login.html", form=form)
        else:
            user_password = user.get("passwrdHash")
            if check_password_hash(user_password, password):
                session["username"] = username
                flash("You have successfully logged in.", "success")
                return redirect(url_for("admin_.admin_content_update"))
            else:
                flash("Incorrect Password.", "warning")
                return render_template("admin_login.html", form=form)
    print("User:", session.get("username"))
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    {"title": "Error", "message": f"Error in {field}:{error}"},
                    "error",
                )
    return render_template("admin_login.html", form=form, user=current_user)


@admin_.route("/admin/logout", methods=["GET", "POST"])
def admin_logout():
    if "username" in session:
        session.pop("username")
    flash("You have successfully logged out.", "success")
    return redirect(url_for("admin_.admin_login"))



env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)
mail_api_key = os.environ.get("MAIL_API_KEY")
mail_api_secret_key = os.environ.get("MAIL_API_SECRET_KEY")


mailjet = Client(auth=(mail_api_key, mail_api_secret_key), version="v3.1")


@admin_.route("/admin/newsfeed/send-emails", methods=["GET", "POST"])
@admin_login_required
def admin_newsfeed():
    mongo = get_mongo(app)
    sender_username = session["username"]
    sender_name = mongo.users.find_one({"username": sender_username}).get("name")

    form = AdminSendEmailForm()
    emails = mongo.newsfeed.find()
    all_emails = []
    for email in emails:
        all_emails.append(email.get("email"))
    if form.validate_on_submit():
        email = form.email.data  # recipient's email
        subject = form.subject.data  # subject of the email
        message = form.message.data  # message to send

        # If email field is empty, send to all emails
        if not email:
            for email in all_emails:
                send_email(sender_name,email, subject, message)
        else:
            send_email(sender_name,email,  subject, message)

    return render_template(
        "admin_newsfeed.html",
        form=form,
    )


def send_email(sender, email, subject, message):
    data = {
        "Messages": [
            {
                "From": {"Email": sender},  # Fix here: Removed extra curly braces
                "To": [{"Email": email, "Name": "Recipient's Name"}],
                "Subject": subject,
                "TextPart": message,
                "HTMLPart": "<h3>{}</h3>".format(message),
            }
        ]
    }
    result = mailjet.send.create(data=data)
    if result.status_code == 200:
        print("Email sent successfully")
    else:
        print("Failed to send email")



@admin_.route("/admin/messages", methods=["GET"])
@admin_login_required
def admin_messages():
    mongo = get_mongo(app)
    messages = mongo.customer.find()
    messages_data=[]
    for message in messages:
        messages_data.append(
            {
            "name": message.get("name"),
            "email": message.get("email"),
            "subject": message.get("subject"),
            "message": message.get("message"),
            "date": message.get("dateOfRegister"),
            }
        )
    
    return render_template("admin_messages.html", messages_data=messages_data, user=current_user)

@admin_.route("/admin", methods=["POST"])
@admin_.route("/admin/content/update", methods=["GET", "POST"])
@admin_login_required
def admin_content_update():
    if not session.get("username"):
        flash("You need to login first.", "warning")
        return redirect(url_for("admin_.admin_login"))
    else:
        flash("You have successfully logged in.", "success")
        mongo = get_mongo(app)
        slider_data = []
        for slider in mongo.slider.find():
            slider_data.append(
                {
                    "title": slider.get("title"),
                    "description": slider.get("description"),
                    "contact_link": slider.get("contact_link"),
                    "image": slider.get("image"),
                    "quote_link": slider.get("quote_link"),
                    "id": slider.get("_id"),
                }
            )
        print(slider_data)

        about_data = []
        for about in mongo.about.find():
            about_data.append(
                {
                    "title": about.get("title"),
                    "description": about.get("description"),
                    "image": about.get("image"),
                    "id": about.get("_id"),
                }
            )

        team_data = []
        for team in mongo.team.find():
            team_data.append(
                {
                    "name": team.get("name"),
                    "description": team.get("description"),
                    "image": team.get("image"),
                    "link_fb": team.get("link_fb"),
                    "link_tw": team.get("link_tw"),
                    "link_linkedin": team.get("link_linkedin"),
                    "link_insta": team.get("link_insta"),
                    "id": team.get("_id"),
                }
            )
        work_data = []
        for work in mongo.work.find():
            work_data.append(
                {
                    "title": work.get("title"),
                    "description": work.get("description"),
                    "service_title": work.get("service_title"),
                    "service_description": work.get("service_description"),
                    "read": work.get("read"),
                    "image": work.get("image"),
                    "id": work.get("_id"),
                }
            )

        contact_data = []
        for contact in mongo.contact.find():
            contact_data.append(
                {
                    "telephone": contact.get("telephone"),
                    "email": contact.get("email"),
                    "id": contact.get("_id"),
                }
            )
        client_data = []
        for client in mongo.clients.find():
            client_data.append(
                {
                    "title": client.get("title"),
                    "description": client.get("description"),
                    "client_title": client.get("service_title"),
                    "client_description": client.get("service_description"),
                    "read": client.get("read"),
                    "image": client.get("image"),
                    "id": client.get("_id"),
                }
            )
        service_data = []
        for service in mongo.service.find():
            service_data.append(
                {
                    "title": service.get("title"),
                    "description": service.get("description"),
                    "service_title": service.get("service_title"),
                    "service_description": service.get("service_description"),
                    "read": service.get("read"),
                    "image": service.get("image"),
                    "id": service.get("_id"),
                }
            )
        footer_data = []
        for footer in mongo.footer.find():
            footer_data.append(
                {
                    "title": footer.get("title"),
                    "description": footer.get("description"),
                    "link_facebook": footer.get("link_facebook"),
                    "link_twitter": footer.get("link_twitter"),
                    "link_linkedin": footer.get("link_linkedin"),
                    "link_youtube": footer.get("link_youtube"),
                    "id": footer.get("_id"),
                }
            )

        return render_template(
            "admin_content_update.html",
            admin="admin",
            slider_data=slider_data,
            about_data=about_data,
            team_data=team_data,
            contact_data=contact_data,
            client_data=client_data,
            work_data=work_data,
            service_data=service_data,
            footer_data=footer_data,
        )


@admin_.route("/admin/content/update/slider", methods=["GET", "POST"])
@admin_login_required
def admin_content_update_slider():
    mongo = get_mongo(app)
    slider = mongo.slider.find_one()
    form = AdminEditSliderForm()
    if form.validate_on_submit():
        slider_form_title = form.title.data
        slider_form_description = form.description.data
        slider_contact_link = form.contact_link.data
        slider_form_quote_link = form.quote_link.data
        image = form.image.data
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.static_folder, filename))
        slider_form_image = filename
        slider = Slider(
            slider_form_title,
            slider_form_description,
            filename,
            slider_contact_link,
            slider_form_quote_link,
            mongo,
        )
        slider.save()
        flash({"message": "Successfully updated slider"}, "success")
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    {"title": "Error", "message": f"Error in {field}:{error}"},
                    "error",
                )
    return render_template(
        "admin_content_update_slider.html",
        admin="admin",
        slider=slider,
        form=form,
    )


@admin_.route("/admin/content/update/about", methods=["GET", "POST"])
@admin_login_required
def admin_content_update_about():
    mongo = get_mongo(app)
    about = mongo.about.find_one()
    form = AdminEditAboutForm()
    if form.validate_on_submit():
        about_form_title = form.title.data
        about_form_description = form.description.data
        about_form_read = form.read.data
        image = form.image.data
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.static_folder, filename))

        about = About(
            about_form_title, about_form_description, about_form_read, filename, mongo
        )
        about.save()
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    {"title": "Error", "message": f"Error in {field}:{error}"},
                    "error",
                )
    return render_template(
        "admin_content_update_about.html",
        admin="admin",
        about=about,
        form=form,
    )


@admin_.route("/admin/content/update/team", methods=["GET", "POST"])
@admin_login_required
def admin_content_update_team():
    mongo = get_mongo(app)
    team = mongo.team.find_one()
    form = AdminEditTeamForm()
    if form.validate_on_submit():
        team_form_title = form.name.data
        team_form_description = form.description.data
        team_form_link_fb = form.link_fb.data
        team_form_link_twitter = form.link_tw.data
        team_form_link_linkedin = form.link_linkedin.data
        team_form_link_insta = form.link_insta.data
        image = form.image.data
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.static_folder, filename))

        team = Team(
            team_form_title,
            team_form_description,
            filename,
            team_form_link_fb,
            team_form_link_twitter,
            team_form_link_linkedin,
            team_form_link_insta,
            mongo,
        )
        team.save()
        flash({"message": "Successfully updated team"}, "success")
    return render_template(
        "admin_content_update_team.html",
        admin="admin",
        team=team,
        form=form,
    )


@admin_.route("/admin/content/update/contact", methods=["GET", "POST"])
@admin_login_required
def admin_content_update_contact():
    mongo = get_mongo(app)
    contact = mongo.contact.find_one()
    form = AdminEditContactForm()
    if form.validate_on_submit():
        contact_form_telephone = form.telephone.data
        contact_form_email = form.email.data
        contact = Contact(contact_form_telephone, contact_form_email, mongo)
        contact.save()
        flash({"message": "Successfully updated contact"}, "success")
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(
                        {"title": "Error", "message": f"Error in {field}:{error}"},
                        "error",
                    )
    return render_template(
        "admin_content_update_contact.html",
        admin="admin",
        contact=contact,
        form=form,
    )


@admin_.route("/admin/content/update/service", methods=["GET", "POST"])
@admin_login_required
def admin_content_update_service():
    mongo = get_mongo(app)
    service = mongo.service.find_one()
    form = AdminEditServiceForm()
    if form.validate_on_submit():
        service_form_title = form.title.data
        service_form_description = form.description.data
        service_form_service_title = form.service_title.data
        service_form_service_description = form.service_description.data
        service_form_read = form.read.data
        image = form.image.data
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.static_folder, filename))
        service = Service(
            service_form_title,
            service_form_description,
            service_form_service_title,
            service_form_service_description,
            service_form_read,
            filename,
            mongo,
        )
        service.save()
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    {"title": "Error", "message": f"Error in {field}:{error}"},
                    "error",
                )
    return render_template(
        "admin_content_update_service.html",
        admin="admin",
        service=service,
        form=form,
    )


@admin_.route("/admin/content/update/work", methods=["GET", "POST"])
@admin_login_required
def admin_content_update_work():
    mongo = get_mongo(app)
    work = mongo.work.find_one()
    form = AdminEditWorkForm()
    if form.validate_on_submit():
        work_form_title = form.title.data
        work_form_description = form.description.data
        work_form_service_title = form.service_title.data
        work_form_service_description = form.service_description.data
        work_form_read = form.read.data
        image = form.image.data
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.static_folder, filename))

        work = Work(
            work_form_title,
            work_form_description,
            work_form_service_title,
            work_form_service_description,
            work_form_read,
            filename,
            mongo,
        )
        work.save()
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    {"title": "Error", "message": f"Error in {field}:{error}"},
                    "error",
                )
    return render_template(
        "admin_content_update_work.html",
        admin="admin",
        work=work,
        form=form,
    )


@admin_.route("/admin/content/update/footer", methods=["GET", "POST"])
@admin_login_required
def admin_content_update_footer():
    mongo = get_mongo(app)
    footer = mongo.footer.find_one()
    form = AdminEditFooterForm()
    if form.validate_on_submit():
        footer_form_title = form.title.data
        footer_form_description = form.description.data
        footer_form_link_fb = form.link_facebook.data
        footer_form_link_twitter = form.link_twitter.data
        footer_form_link_linkedin = form.link_linkedin.data
        footer_form_link_youtube = form.link_youtube.data

        footer = Footer(
            footer_form_title,
            footer_form_description,
            footer_form_link_fb,
            footer_form_link_twitter,
            footer_form_link_linkedin,
            footer_form_link_youtube,
            mongo,
        )
        footer.save()
        flash({"message": "Successfully updated footer"}, "success")
    return render_template(
        "admin_content_update_footer.html",
        admin="admin",
        footer=footer,
        form=form,
    )


@admin_.route("/admin/content/update/client", methods=["GET", "POST"])
@admin_login_required
def admin_content_update_client():
    mongo = get_mongo(app)
    client = mongo.clients.find_one()
    form = AdminEditClientForm()

    if form.validate_on_submit():
        client_form_title = form.title.data
        client_form_description = form.description.data
        client_form_service_title = form.client_title.data
        client_form_service_description = form.client_description.data
        client_form_read = form.read.data
        image = form.image.data
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.static_folder, filename))

        client = Clients(
            client_form_title,
            client_form_description,
            client_form_service_title,
            client_form_service_description,
            client_form_read,
            filename,
            mongo,
        )
        client.save()
        flash({"message": "Successfully updated client"}, "success")
    return render_template(
        "admin_content_update_client.html",
        admin="admin",
        client=client,
        form=form,
    )


@admin_.route("/admin/content/delete/footer/<id>", methods=["POST"])
def admin_delete_footer(id):
    mongo = get_mongo(app)
    footer = mongo.footer.find_one({"_id": ObjectId(id.strip("}"))})
    if footer:
        mongo.footer.delete_one({"_id": ObjectId(id.strip("}"))})
        flash({"message": "Footer Deleted"}, "warning")
        return redirect(url_for("admin_.admin_content_update"))
    else:
        flash({"message": "Footer not found"}, "error")
    return redirect(url_for("admin_.admin_content_update_footer"))


@admin_.route("/admin/content/delete/client/<id>", methods=["POST"])
def admin_delete_client(id):
    mongo = get_mongo(app)
    client = mongo.clients.find_one({"_id": ObjectId(id.strip("}"))})
    print("Client:", id)
    if client:
        mongo.clients.delete_one({"_id": ObjectId(id.strip("}"))})
        flash({"message": "Client Deleted"}, "warning")
        return redirect(url_for("admin_.admin_content_update"))
    else:
        flash({"message": "Client not found"}, "error")
    return redirect(url_for("admin_.admin_content_update_client"))


@admin_.route("/admin/content/delete/work/<id>", methods=["POST"])
def admin_delete_work(id):
    mongo = get_mongo(app)
    work = mongo.work.find_one({"_id": ObjectId(id.strip("}"))})
    if work:
        mongo.work.delete_one({"_id": ObjectId(id.strip("}"))})
        flash({"message": "Work Deleted"}, "warning")
        return redirect(url_for("admin_.admin_content_update"))
    else:
        flash({"message": "Work not found"}, "error")

    return redirect(url_for("admin_.admin_content_update_work"))


@admin_.route("/admin/content/delete/service/<id>", methods=["POST"])
def admin_delete_service(id):
    mongo = get_mongo(app)
    service = mongo.service.find_one({"_id": ObjectId(id.strip("}"))})
    if service:
        mongo.service.delete_one({"_id": ObjectId(id.strip("}"))})
        flash({"message": "Service Deleted"}, "warning")
        return redirect(url_for("admin_.admin_content_update"))
    else:
        flash({"message": "Service not found"}, "error")
    return redirect(url_for("admin_.admin_content_update_service"))


@admin_.route("/admin/content/delete/contact/<id>", methods=["POST"])
def admin_delete_contact(id):
    mongo = get_mongo(app)
    contact = mongo.contact.find_one({"_id": ObjectId(id.strip("}"))})
    if contact:
        mongo.contact.delete_one({"_id": ObjectId(id.strip("}"))})
        flash({"message": "Contact Deleted"}, "warning")
        return redirect(url_for("admin_.admin_content_update"))
    else:
        flash({"message": "Contact not found"}, "error")
    return redirect(url_for("admin_.admin_content_update_contact"))


@admin_.route("/admin/content/delete/team/<id>", methods=["POST"])
def admin_delete_team(id):
    mongo = get_mongo(app)
    team = mongo.team.find_one({"_id": ObjectId(id.strip("}"))})
    if team:
        mongo.team.delete_one({"_id": ObjectId(id.strip("}"))})
        flash({"message": "Team Deleted"}, "warning")
        return redirect(url_for("admin_.admin_content_update"))
    else:
        flash({"message": "Team not found"}, "error")
    return redirect(url_for("admin_.admin_content_update_team"))


@admin_.route("/admin/content/delete/about/<id>", methods=["POST"])
def admin_delete_about(id):
    mongo = get_mongo(app)
    about = mongo.about.find_one({"_id": ObjectId(id.strip("}"))})
    if about:
        mongo.about.delete_one({"_id": ObjectId(id.strip("}"))})
        flash({"message": "About Deleted"}, "warning")
        return redirect(url_for("admin_.admin_content_update"))
    else:
        flash({"message": "About not found"}, "error")
    return redirect(url_for("admin_.admin_content_update_about"))


@admin_.route("/admin/content/delete/slider/<id>", methods=["POST"])
def admin_delete_slider(id):
    mongo = get_mongo(app)
    slider = mongo.slider.find_one({"_id": ObjectId(id.strip("}"))})
    if slider:
        mongo.slider.delete_one({"_id": ObjectId(id.strip("}"))})
        flash({"message": "Slider Deleted"}, "warning")
        return redirect(url_for("admin_.admin_content_update"))
    else:
        flash({"message": "Slider not found"}, "error")
    return redirect(url_for("admin_.admin_content_update_slider"))


@admin_.route("/admin/users", methods=["GET", "POST"])
@admin_login_required
def admin_users():
    mongo = get_mongo(app)
    user_collection = mongo.users
    users = []
    for user in user_collection.find():
        user_dict = {
            "id": str(user.get("_id")),  # Convert ObjectId to str
            "username": user.get("username"),
            "email": user.get("email"),
            "name": user.get("name"),
            "dateOfRegister": user.get("dateOfRegister"),
            "is_Admin": user.get("is_Admin"),
        }
        users.append(user_dict)

    return render_template(
        "admin_users.html",
        users=users,
    )


@admin_.route("/admin/create-user", methods=["GET", "POST"])
@admin_login_required
def admin_create_user():
    mongo = get_mongo(app)
    form = AdminUserCreateForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        admin = request.form.get("admin")
        existing_username = mongo.db.users.find_one({"username": username})
        if existing_username:
            flash({"message": "This Username is already taken"}, "warning")
            return render_template("admin_create_user.html", form=form)
        user = User(username, password, admin)
        user.save()
        flash({"message": "Succefully created a user"}, "success")

    if form.errors:
        flash(f"{form.errors}", "warning")
    return render_template(
        "admin_create_user.html",
        form=form,
    )


@admin_.route("/admin/user-update/<id>", methods=["GET", "POST"])
@admin_login_required
def admin_update_user(id):
    mongo = get_mongo(app)
    form = AdminUserUpdateForm()
    user = mongo.users.find_one({"_id": ObjectId(id.strip("}"))})
    user_id = user.get("_id")
    # Convert id to ObjectId
    print("User:", user)
    if form.validate_on_submit():
        flash({"message": "Successfully updated user"}, "success")
        updated_user = {
            "username": form.username.data,
            "email": form.email.data,
            "name": form.name.data,
            "is_Admin": form.admin.data,
        }
        # Save the updated user document
        mongo.users.update_one({"_id": ObjectId(id.strip("}"))}, {"$set": updated_user})
        flash({"message": "Successfully updated user"}, "success")
        return redirect(url_for("admin_.admin_users"))
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    {"title": "Error", "message": f"Error in {field}:{error}"},
                    "error",
                )
    return render_template(
        "admin_user_update.html",
        form=form,
        user_id=user_id,
    )


@admin_.route("/admin/user-delete/<id>", methods=["POST"])
@admin_login_required
def admin_delete_user(id):
    mongo = get_mongo(app)
    user = mongo.users.find_one({"_id": ObjectId(id)})

    if user:
        mongo.users.delete_one({"_id": ObjectId(id)})
        flash({"message": "User Deleted"}, "warning")
    else:
        flash({"message": "User not found"}, "error")
    return redirect(url_for("admin_.admin_users"))
