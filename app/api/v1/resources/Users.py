from flask_restful import Resource, reqparse, marshal_with, marshal
from app.models import User
from .fields import user_fields
from app.auth import Auth
from flask import abort

from .fields import UserSchema

class Users(Resource):
    """
    This is the class deals with users
    """
    #@marshal_with(user_fields, envelope="user")
    def get(self, id):
        user = User.query.filter(User.id == id).first()
        print(type(User))
        # if user is not None:
        #     return user
        # else:
        #     abort(404)
        #return user if user is not None else abort(404)
        schema = UserSchema()
        result = schema.dump(user)
        return result.data

