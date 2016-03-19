# Import main Flask app instance, Blueprint, flask_restful
from flask import Blueprint, jsonify
from app import app
from flask_restful import Resource, Api
from .resources.noticelist import NoticeList
from .resources.notice import Notice
from .resources.UserAuth import UserAuth
from .resources.UserManager import UserManager
from .resources.RegistrationManager import RegistrationManager
from .resources.UserSelf import UserSelf
from app.exceptions import InvalidUsage


# Define Blueprint of api
apiv1_bp = Blueprint('apiv1', __name__)

# Create restful Api using the blueprint
apiv1 = Api(apiv1_bp)

# Add url to notices class
apiv1.add_resource(NoticeList, '/notices/', endpoint='notices')
# Add resource single notice to rest api
apiv1.add_resource(Notice, '/notice/<int:id>', endpoint='notice')

# Add login/userauth resource to rest api
apiv1.add_resource(UserAuth, '/login', endpoint='login')

# Add User resource to rest api
apiv1.add_resource(UserManager, '/users/<int:id>', '/users', endpoint='user')

# Add register url
apiv1.add_resource(RegistrationManager, '/register', endpoint='register')

# Add current user info url
apiv1.add_resource(UserSelf, '/user', endpoint='selfuser')

# Register error handler
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response