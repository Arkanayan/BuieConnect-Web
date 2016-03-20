from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from app import Auth
from app.Auth import get_info_from_google_id_token, check_user_exists, generate_token
from .fields import LoginSchema, ErrorSchema, Error
from flask import request, g
from flask_restful import marshal
from flask_marshmallow import pprint
from .utils import get_error_json, get_users_json, get_token_json_output
from app.exceptions import UserNotFound, ErrorNoIdToken, InvalidUsage
from .RegistrationManager import RegistrationManager


class UserAuth(Resource):
    """ Handles users authentication, login etc."""

    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        pass

    def post(self):
        """
        Handles login function
        which is get auth token
        :return: Auth token
        """
        try:
            login_schema = LoginSchema(strict=True)
            result = login_schema.load(request.get_json())
            if len(result.data) < 1:
                raise ErrorNoIdToken
        except ValidationError:
            raise ErrorNoIdToken
        except:
            raise ErrorNoIdToken

        data = result.data
        id_token = data['id_token']
        google_info = get_info_from_google_id_token(id_token=id_token)
        try:
            user = check_user_exists(google_info['sub'])
            token = user.get_auth_token()
            return get_token_json_output(token)
        except:
            raise UserNotFound
