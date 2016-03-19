from flask_restful import Resource
from app import Auth
from flask import g
from .utils import get_users_json

class UserSelf(Resource):

    @Auth.require_login
    def get(self):
        # get current user from g object
        current_user = g.get('user', None)
        return get_users_json(current_user)