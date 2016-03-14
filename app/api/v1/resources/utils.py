from app.models import User
from .fields import ErrorSchema,Error, UserSchema
from app.models import User


def get_error_json(message="There is an error.", code=400):
    error_schema = ErrorSchema()
    error = Error(message=message, code=code)
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