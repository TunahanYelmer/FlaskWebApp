from flask import  render_template
from seotech_app import app 

@app.route('', methods=['GET', 'POST'])
def home():
    render_template('index.html')
@app.route('/about', methods=['GET', 'POST'])
def about():
    render_template('about.html')
@app.route('/service',methods=['GET','POST'])
def service():
    return render_template('service.html')
