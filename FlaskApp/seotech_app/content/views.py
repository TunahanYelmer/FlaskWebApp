from flask import render_template, Blueprint

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", home="home",)

@main.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html", about="about" ,) 

@main.route("/service", methods=["GET", "POST"])
def service():
    return render_template("service.html", service="service" ,) 
