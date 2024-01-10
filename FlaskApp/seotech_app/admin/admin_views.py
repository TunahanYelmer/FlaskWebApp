from flask import render_template, Blueprint

admin_ =Blueprint("admin", __name__)

@admin_.route("/admin", methods=["GET", "POST"])
def admin():
    
    return render_template("admin_panel.html", admin="admin" ,)