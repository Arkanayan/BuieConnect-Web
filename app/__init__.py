from flask import Flask
from app.config import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# Define flask app instance
app = Flask(__name__)
# Flask config object from config class
app.config.from_object(DevelopmentConfig)

# Initialize the database
db = SQLAlchemy(app)

# Initialize flask marshmallow object
marsh = Marshmallow(app)

# Import views
from app import views

from app.api.v1 import apiv1_bp
# Register blueprint and new url will be site.com/api/v1/*
app.register_blueprint(apiv1_bp, url_prefix='/api/v1')

# import and register admin blueprint
from app.admin import admin_bp
app.register_blueprint(admin_bp)
