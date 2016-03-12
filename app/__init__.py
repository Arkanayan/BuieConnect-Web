from flask import Flask
from app.config import *

# Define flask app instance
app = Flask(__name__)
# Flask config object from config class
app.config.from_object(DevelopmentConfig)

# Import views
from app.api import v1
from app import views

