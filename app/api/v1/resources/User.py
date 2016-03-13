from flask_restful import Resource, reqparse, marshal_with
from app.models import User
from .fields import user_fields
from app.auth import get_user_from_id

class User(Resource):

    @marshal_with(user_fields)
    def get(self, id):
        user = get_user_from_id(id)
        return user
