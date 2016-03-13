from flask_restful import Resource, reqparse, marshal_with, marshal
from app.models import User
from .fields import user_fields
from app.auth import Auth
from flask import abort
from marshmallow import pprint

from .fields import UserSchema

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
            users = User.query.limit(5).all()
            many = True if len(users) > 1 else False
            result = self.schema.dump(users, many=many)
            #pprint(result.data)
            return result.data
        if id is not None and limit is None:
            user = User.query.filter(User.id == id).first()
            result = self.schema.dump(user)
            return result.data
        if id is not None and limit is not None:
            users = User.query.offset(id-1).limit(limit).all()
            print(len(users))
            many = True if len(users) > 1 else False
            #user = [users[0] if len(users) <= 1 else users]
            user = self.get_currect_num_items(users)
            result = self.schema.dump(user, many=many)
        #print(user.email)
        # if user is not None:
        #     return user
        # else:
        #     abort(404)
        #return user if user is not None else abort(404)
            pprint(result.data)
            return result.data

    def get_currect_num_items(self, items):
        if len(items) <= 1:
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


