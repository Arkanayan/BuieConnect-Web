from flask import Flask
from app.config import *
from flask.ext.sqlalchemy import SQLAlchemy

# Define flask app instance
app = Flask(__name__)
# Flask config object from config class
app.config.from_object(DevelopmentConfig)

# Initialize the database
db = SQLAlchemy(app)


# Import views
from app import views

from app.api.v1 import apiv1_bp
# Register blueprint and new url will be site.com/api/v1/*
app.register_blueprint(apiv1_bp, url_prefix='/api/v1')


