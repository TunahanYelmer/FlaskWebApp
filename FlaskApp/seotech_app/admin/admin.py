from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from seotech_app.__init__ import app, db
from seotech_app.admin.admin_models import User

# Create admin
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

# Add views
admin.add_view(ModelView(User, db.session))
