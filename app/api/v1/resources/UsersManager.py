from flask_restful import Resource
from app.models import User
from .fields import UserSchema

class UsersManager(Resource):
    def get(self):
        pass

