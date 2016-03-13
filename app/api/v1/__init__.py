# Import main Flask app instance, Blueprint, flask_restful
from flask import Blueprint
from app import app
from flask_restful import Resource, Api
from .resources.noticelist import NoticeList
from .resources.notice import Notice

# Define Blueprint of api
apiv1_bp = Blueprint('apiv1', __name__)

# Create restful Api using the blueprint
apiv1 = Api(apiv1_bp)

# Add url to articles class
apiv1.add_resource(NoticeList, '/notices/', endpoint='notices')
# Add resource single Article to restr api
apiv1.add_resource(Notice, '/notice/<int:id>', endpoint='notice')


