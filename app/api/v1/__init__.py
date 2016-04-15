# Import main Flask app instance, Blueprint, flask_restful
from flask import Blueprint, jsonify
from flask_restful import Api

from app import app
from app.api.v1.resources.admin_urls.MessageHandler import MessageHandler
from app.api.v1.resources.admin_urls.Verify import Verify
from app.exceptions import InvalidUsage
from .resources.RegistrationManager import RegistrationManager
from .resources.UserAuth import UserAuth
from .resources.UserManager import UserManager
from .resources.UserSelf import UserSelf
from .resources.notice import Notice
from .resources.Notices import NoticeList

# Define Blueprint of api
apiv1_bp = Blueprint('apiv1', __name__)

# Create restful Api using the blueprint
apiv1 = Api(apiv1_bp)

# Add url to notices class
apiv1.add_resource(NoticeList, '/notices/', '/notices/<int:id>', endpoint='notices')
# Add resource single notice to rest api
# apiv1.add_resource(NoticeList, '/notices/<int:id>', endpoint='notices')

# Add login/userauth resource to rest api
apiv1.add_resource(UserAuth, '/login', endpoint='login')

# Add User resource to rest api
apiv1.add_resource(UserManager, '/users/<int:id>', '/users', endpoint='user')

# Add register url
apiv1.add_resource(RegistrationManager, '/register', endpoint='register')

# Add current user info url
apiv1.add_resource(UserSelf, '/user', endpoint='selfuser')

# Add admin verification api
apiv1.add_resource(Verify, '/admin/verified', endpoint='admin')
apiv1.add_resource(Verify, '/admin/verify', methods=['POST'], endpoint='verify_user')

#Add message sending admin api
apiv1.add_resource(MessageHandler, '/admin/send', endpoint='message_handler')

# Register error handler
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response