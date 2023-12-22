from flask import render_template, Blueprint

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", home="home", show_slider=True)

@main.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html", about="about" ,show_slider=True) 

@main.route("/service", methods=["GET", "POST"])
def service():
    return render_template("service.html", service="service" ,show_slider=False) 
