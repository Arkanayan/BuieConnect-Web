from flask_restful import Resource, reqparse, marshal_with, marshal
from app.models import User
from .fields import user_fields
from app.auth import Auth
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


    #@marshal_with(user_fields, envelope="user")
    def get(self, id=None, limit=None):
        if id is None and limit is None:
            try:
                users = User.query.limit(5).all()
            except:
                get_error_json("Users not found", 404)
            many = True if len(users) > 1 else False
            # result = self.schema.dump(users, many=many)
            #pprint(result.data)
            return get_users_json(users, many)
        if id is not None and limit is None:
            try:
                user = User.query.filter(User.id == id).first()
                if user is None:
                    raise UserNotFound
                return get_users_json(user, False)
            except:
                return get_error_json("User not found", 404)
            # result = self.schema.dump(user)
        if id is not None and limit is not None:
            try:
                users = User.query.offset(id-1).limit(limit).all()
            except:
                return get_error_json("User not found", 404)
            print(len(users))
            many = True if len(users) > 1 else False
            #user = [users[0] if len(users) <= 1 else users]
            #user = self.get_currect_num_items(users)
            #result = self.schema.dump(user, many=True)
        #print(user.email)
        # if user is not None:
        #     return user
        # else:
        #     abort(404)
        #return user if user is not None else abort(404)
            #pprint(result.data)
            return get_users_json(users, many)

    def get_currect_num_items(self, items):
        if len(items) >= 1:
            user = items[0]
        else:
            user = items
        return user

    def put(self, id):
        user = Auth.get_user_from_id(id)
        print(len(user))
        many = self.if_many(user)
        user = self.get_currect_num_items(user)
        result = self.schema.dump(user, many=many)
        return result.data


