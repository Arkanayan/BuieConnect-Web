from app.models import User
from .fields import ErrorSchema,Error, UserSchema
from app.models import User
from flask import jsonify

def get_error_json(message="There is an error.", code=400, additional_errors=[]):
    error_schema = ErrorSchema(many=False)
    error = Error(message=message, code=code, errors=additional_errors)
    return error_schema.dump(error).data, code

def get_users_json(users, many=False):
    """
    Serialized users json output
    :param users: user(s) object
    :param many: multiple users or not
    :returns: Serialized users json output
    """
    user_schema = UserSchema()
    result = user_schema.dump(users, many=many)
    return result.data


def get_token_json_output(token, first_time=False):
    """
    Get jsonified token string for output
    :param token: auth token
    :param first_time if the user registerd this time
    :return: jsonified token string
    """
    return jsonify({'auth_token': token,
                    'first_time': first_time})
