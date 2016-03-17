from flask_restful import Resource, reqparse, marshal_with, marshal, originaflask_make_response
from app.models import User, Error
from .fields import user_fields
from app import Auth
from flask import abort
from marshmallow import pprint
from app.models import Error
from .fields import UserSchema, ErrorSchema
from .utils import get_error_json, get_users_json
from app.exceptions import UserNotFound

class UserManager(Resource):
    """
    This is the class deals with users
    """
    def __init__(self):
        self.schema = UserSchema()

    def if_many(self, items):
        many = True if len(items) > 1 else False
        return many


    #@marshal_with(user_fields)
    def get(self, id=None):
        if id is None:
            try:
                users = User.query.limit(5).all()
            except:
                get_error_json("Users not found", 404)
            # result = self.schema.dump(users, many=many)
            #pprint(result.data)
            return get_users_json(users, many=True)
        if id is not None:
            try:
                user = User.query.filter(User.id == id).first()
                if user is None:
                    raise UserNotFound
                return get_users_json(user, False)
            except:
                return get_error_json("User not found", 404)

    def get_currect_num_items(self, items):
        if len(items) >= 1:
            user = items[0]
        else:
            user = items
        return user

    @Auth.require_admin
    def put(self, id=None):
        if id is None:
            return get_error_json("Please provide an user id", 400)
        user = Auth.get_user_from_id(id)
        print(len(user))
        many = self.if_many(user)
        user = self.get_currect_num_items(user)
        result = self.schema.dump(user, many=many)
        return result.data

    def post(self):
        list = [
            Error("this is error 1", 401),
            Error("This is error 2", 405)
        ]
        error = Error("This is main error", 201, list)
        return get_error_json("This is main error", 400, list)


