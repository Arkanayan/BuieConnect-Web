from flask_restful import Resource
from .fields import RegistraionDataSchema, LoginSchema
from flask import request
from marshmallow import pprint, ValidationError
from app.exceptions import InvalidUsage, UserNotFound, UserCannotRegister
from app.Auth import get_info_from_google_id_token, register_user, check_user_exists, generate_token
from .utils import get_users_json, get_token_json_output


class RegistrationManager(Resource):

    def post(self):
        """
        Registers / logins user
        :return token: auth token
        """
        try:
            result = LoginSchema(strict=True).load(request.get_json())
            pprint(result.data)
        except ValidationError as err:
            raise InvalidUsage("Please provide the id_token")

        data = result.data
        id_token = data['id_token']
        google_info = get_info_from_google_id_token(id_token=id_token)
        try:
            user = check_user_exists(google_info['sub'])
            token = generate_token(get_users_json(user))
            return get_token_json_output(token)
        except UserNotFound:
            user = register_user(google_info)
            return get_users_json(user)
        except:
            raise UserCannotRegister