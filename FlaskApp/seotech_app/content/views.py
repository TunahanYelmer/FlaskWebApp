from flask import (
    request,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    Blueprint,
    current_app as app,
)
from seotech_app.content.models import (
    Customer,
    NewsLetter,
    NewsLetterForm,
    CustomerMessageForm,
    get_mongo,
)


main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def home():
    mongo = get_mongo(app)
    form = CustomerMessageForm()
    newsform = NewsLetterForm()
    slider_data = []
    for slider in mongo.slider.find():
        slider_data.append(
            {
                "title": slider.get("title"),
                "description": slider.get("description"),
                "contact_link": slider.get("contact_link"),
                "quote_link": slider.get("quote_link"),
                "image": slider.get("image"),
                
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
            }
        )

    contact_data = []
    for contact in mongo.contact.find():
        contact_data.append(
            {
                "telephone": contact.get("telephone"),
                "email": contact.get("email"),
            }
        )
    client_data = []
    for client in mongo.clients.find():
        client_data.append(
            {
                "title": client.get("title"),
                "description": client.get("description"),
                "service_title": client.get("client_title"),
                "service_description": client.get("client_description"),
                "read": client.get("read"),
                "image": client.get("image"),
            }
        )
        for client in client_data:
            print("client image:", client["image"])
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
            }
        )
        print(service.get("image"))
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
            }
        )
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        customer = Customer(name, email, subject, message, mongo)
        customer.save()

        return redirect(url_for("main.home"))

    if newsform.validate_on_submit():
        email = newsform.email.data
        newsletter = NewsLetter(email, mongo)
        newsletter.save()

        return redirect(url_for("main.home"))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    {"title": "Error", "message": f"Error in {field}:{error}"},
                    "error",
                )
    return render_template(
        "home.html",
        home="home",
        form=form,
        newsform=newsform,
        slider_data=slider_data,
        about_data=about_data,
        service_data=service_data,
        team_data=team_data,
        contact_data=contact_data,
        work_data=work_data,
        client_data=client_data,
        footer_data=footer_data,
    )


@main.route("/about", methods=["GET", "POST"])
def about():
    mongo = get_mongo(app)
    form = CustomerMessageForm()
    newsform = NewsLetterForm()
    about_data = []
    for about in mongo.about.find():
        about_data.append(
            {
                "title": about.get("title"),
                "description": about.get("description"),
                "image": about.get("image"),
            }
        )

    contact_data = []
    for contact in mongo.contact.find():
        contact_data.append(
            {
                "telephone": contact.get("telephone"),
                "email": contact.get("email"),
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
            }
        )
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        customer = Customer(name, email, subject, message, mongo)
        customer.save()

        return redirect(url_for("main.home"))

    if newsform.validate_on_submit():
        email = newsform.email.data
        newsletter = NewsLetter(email, mongo)
        newsletter.save()

        return redirect(url_for("main.home"))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    {"title": "Error", "message": f"Error in {field}:{error}"},
                    "error",
                )
    return render_template(
        "about.html",
        home="home",
        form=form,
        newsform=newsform,
        about_data=about_data,
        contact_data=contact_data,
        footer_data=footer_data,
    )


@main.route("/service", methods=["GET", "POST"])
def service():
    mongo = get_mongo(app)
    form = CustomerMessageForm()
    newsform = NewsLetterForm()
    slider_data = []
    for slider in mongo.slider.find():
        slider_data.append(
            {
                "title": slider.get("title"),
                "description": slider.get("description"),
                "contact_link": slider.get("contact_link"),
                "image": slider.get("image"),
                "quote_link": slider.get("quote_link"),
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
            }
        )

    contact_data = []
    for contact in mongo.contact.find():
        contact_data.append(
            {
                "telephone": contact.get("telephone"),
                "email": contact.get("email"),
            }
        )
    client_data = []
    for client in mongo.clients.find():
        client_data.append(
            {
                "title": client.get("title"),
                "description": client.get("description"),
                "service_title": client.get("client_title"),
                "service_description": client.get("client_description"),
                "read": client.get("read"),
                "image": client.get("image"),
            }
        )
        for client in client_data:
            print("client image:", client["image"])
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
            }
        )
        print(service.get("image"))
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
            }
        )
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        customer = Customer(name, email, subject, message, mongo)
        customer.save()

        return redirect(url_for("main.home"))

    if newsform.validate_on_submit():
        email = newsform.email.data
        newsletter = NewsLetter(email, mongo)
        newsletter.save()

        return redirect(url_for("main.home"))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    {"title": "Error", "message": f"Error in {field}:{error}"},
                    "error",
                )
    return render_template(
        "service.html",
        home="home",
        form=form,
        newsform=newsform,
        slider_data=slider_data,
        about_data=about_data,
        service_data=service_data,
        team_data=team_data,
        contact_data=contact_data,
        work_data=work_data,
        client_data=client_data,
        footer_data=footer_data,
    )
