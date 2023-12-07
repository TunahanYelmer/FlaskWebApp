from flask import  render_template , request , Blueprint
from seotech_app.init import app , db

main = Blueprint('main',__name__)

@main.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')
@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
@main.route('/service',methods=['GET','POST'])
def service():
    return render_template('service.html')

