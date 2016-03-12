# Import main Flask app instance, Blueprint, flask_restful
from flask import Blueprint
from app import app
from flask_restful import Resource, Api
from app.api.v1.resources.articles import Articles

# Define Blueprint of api
apiv1_bp = Blueprint('apiv1', __name__)

# Create restful Api using the blueprint
apiv1 = Api(apiv1_bp)

apiv1.add_resource(Articles, '/articles/', endpoint='articles')

app.register_blueprint(apiv1_bp, url_prefix='/api/v1')
