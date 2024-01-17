from flask import Flask
from seotech_app.__init__ import create_app

app = create_app()
print(app)

app.run(debug=True)
