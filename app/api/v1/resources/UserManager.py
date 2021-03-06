from flask_restful import Resource, reqparse, marshal_with, marshal
from app.models import User, Error
from .fields import user_fields, UserUpdateSchema
from app import Auth, db
from flask import abort, g, request
from marshmallow import pprint
from app.models import Error
from .fields import UserSchema, ErrorSchema
from .utils import get_error_json, get_users_json
from app.exceptions import UserNotFound, InvalidUsage, NotAuthorized

class UserManager(Resource):
    """
    This is the class deals with users
    """
    def __init__(self):
        self.schema = UserSchema()

    def if_many(self, items):
        many = True if len(items) > 1 else False
        return many


    #@Auth.require_login
    @Auth.require_me_or_admin
    def get(self, id=None):
        # When url is "/users"
        # returns the list of users
        current_user = g.get('user', None)
        if id is not None:
            user = User.query.filter(User.id == id).first()
            if user is None:
                raise UserNotFound()
            return get_users_json(user, False)

        if current_user.is_admin():
            if id is None:
                try:
                    users = User.query.limit(5).all()
                except:
                    get_error_json("Users not found", 404)
                # result = self.schema.dump(users, many=many)
                #pprint(result.data)
                return get_users_json(users, many=True)
        else:
            raise NotAuthorized


        # when url is /users/<id>
        # returns the particular user at <id>

            # except:
            #     #return get_error_json("User not found", 404)
            #     #raise InvalidUsage("User not found", status_code=404)
            #     errors = {'error1': 'message here', 'error2': 'message error 2'}
            #     raise UserNotFound(errors=[errors, {'2': 'message2'}])


    def get_currect_num_items(self, items):
        if len(items) >= 1:
            user = items[0]
        else:
            user = items
        return user

    @Auth.require_login
    def put(self, id=None):
        if id is None:
            return get_error_json("Please provide an user id", 400)

        current_user = g.get('user', None)
        requested_user = Auth.get_user_from_id(id)
        if Auth.requre_self_or_admin(current_user, requested_user):
            try:
                user_update_schema = UserUpdateSchema(partial=True, strict=True)
                result = user_update_schema.load(request.json)
                db.session.add(result.data)
                db.session.commit()
                return get_users_json(result.data)
            except NotAuthorized:
                raise NotAuthorized
            except:
                raise InvalidUsage("Please check the data", 400)

    def post(self):
        list = [
            Error("this is error 1", 401),
            Error("This is error 2", 405)
        ]
        error = Error("This is main error", 201, list)
        return get_error_json("This is main error", 400, list)


