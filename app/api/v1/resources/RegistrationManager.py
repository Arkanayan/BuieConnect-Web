from flask_restful import Resource
from .fields import RegistraionDataSchema
from flask import request
from marshmallow import pprint, ValidationError
from app.exceptions import InvalidUsage
from app.Auth import get_info_from_google_id_token, register_user
from .utils import get_users_json


class RegistrationManager(Resource):

    def post(self):
        reg_data_schema = RegistraionDataSchema
        try:
            result = RegistraionDataSchema(strict=True).load(request.get_json())
            pprint(result.data)
        except ValidationError as err:
            raise InvalidUsage("Please provide the id_token")

        data = result.data
        id_token = data['id_token']
        google_info = get_info_from_google_id_token(id_token=id_token)
        user = register_user(google_info)
        return get_users_json(user)