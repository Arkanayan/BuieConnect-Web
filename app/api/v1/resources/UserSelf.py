from flask_restful import Resource
from app import Auth, db
from flask import g, request

from app.api.v1.resources.fields import UserUpdateSchema
from app.exceptions import NotAuthorized, InvalidUsage
from .utils import get_users_json

class UserSelf(Resource):

    @Auth.require_login
    def get(self):
        # get current user from g object
        current_user = g.get('user', None)
        return get_users_json(current_user)

    @Auth.require_login
    def put(self):
        current_user = g.get('user', None)
        try:
            user_update_schema = UserUpdateSchema(partial=True, strict=True)
            result = user_update_schema.load(request.json)
            updated_user = result.data
            updated_user.set_modified()
            db.session.add(updated_user)
            db.session.commit()
            return get_users_json(result.data)
        except NotAuthorized:
            raise NotAuthorized
        except:
            raise InvalidUsage("Please check the data", 400, result.errors)