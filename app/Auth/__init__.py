
from app import app, db
from app.models import User, Role
from flask import jsonify, request, g
import jwt
from app.exceptions import UserNotFound, UserCannotRegister, ErrorNoToken, InvalidUsage, NotAuthorized, InvalidToken
from app.api.v1.resources.utils import get_users_json

from flask_restful import Resource
from marshmallow import pprint
from oauth2client import client, crypt

""" Decorators """

def require_login(func):
    from functools import wraps
    @wraps(func)
    def check_token(*args, **kwargs):
        # Check to see if it's in their session
        auth_token = get_token_from_header()
        try:
            user = get_user_from_token(auth_token)
            #print(type(user))
            g.user = user
        except:
            raise InvalidToken
        #print(auth_token)
        # Otherwise just send them where they wanted to go
        return func(*args, **kwargs)
    return check_token


def require_admin(func):
    from functools import wraps
    @wraps(func)
    def check_admin(*args, **kwargs):
        auth_token = get_token_from_header()
        user = get_user_from_token(auth_token)
        g.user = user
        if user is None:
            raise UserNotFound
        if user.is_admin():
            return func(*args, **kwargs)
        else:
            raise NotAuthorized
    return check_admin


def require_roles(*roles):
    def real_require_roles(func):
        from functools import wraps
        @wraps(func)
        def check_roles(*args, **kwargs):
            auth_token = get_token_from_header()
            user = get_user_from_token(auth_token)
            print("email: ", user.email)
            g.user = user
            if user is None:
                raise UserNotFound
            #if set(roles) == set([rol.name for rol in user.roles]):
            if (set([rol.name for rol in user.roles]) & set(roles)) == set(roles):
                return func(*args, **kwargs)
            else:
                raise NotAuthorized
        return check_roles
    return real_require_roles


def require_me_or_admin(func):
    from functools import wraps
    @wraps(func)
    def check_admin(*args, **kwargs):
        auth_token = get_token_from_header()
        user = get_user_from_token(auth_token)
        g.user = user
        if user is None:
            raise NotAuthorized
        if user.is_admin() or kwargs.get('id', None) == user.id:
            return func(*args, **kwargs)
        else:
            raise NotAuthorized
    return check_admin


""" Auth functions """


def check_if_admin(user):
    if "admin" in user.roles:
        return True
    else:
        raise NotAuthorized

def requre_self_or_admin(current_user, requested_user):
    """
    Check if request user is current user or admin
    :param current_user: the user requesting
    :param requested_user: the user rquested
    :return: True if admin or current user else exception InvalidUsage
    """
    if "admin" in current_user.roles:
        is_admin = True
    else:
        is_admin = False
    if current_user is requested_user or is_admin:
        return True
    else:
        raise NotAuthorized



def get_token_from_header():
    """
    Gets the token from the header
    :return: token
    """
    auth_token = request.headers.get('Authorization')
    if auth_token is None:
        raise ErrorNoToken()
    return auth_token



def get_user_from_header():
    """
    Gets user from the header
    :return: user
    """
    token = get_token_from_header()
    return get_user_from_token(token)


def get_user_from_token(token):
    """
    Get user object from the id_token
    :param token:
    :return user object or UserNotFound() error
    """
    try:
        user_string = jwt.decode(token, key=app.config.get('SECRET_KEY'))
    except jwt.InvalidTokenError:
        raise InvalidUsage("Invalid token")
    google_sub = user_string['google_sub']
    user = User.query.filter(User.google_sub == google_sub).first()
    # print("get_user_from_token: email: ", user.email)
    if user is not None:
        g.user = user
        return user
    else:
        raise UserNotFound


def check_valid_user_from_sub(sub):
    user = g.get('user', None)
    if user is None or (sub != user.google_sub):
        raise UserNotFound()
    else:
        return True


def decode_token(token):
    """
    This method decodes the auth token
    :param token:
    :return:
    """
    try:
        user_dict = jwt.decode(token, key=app.config.get('SECRET_KEY'))
        return user_dict
    except:
        return None


# @app.route('/secret')
# @require_api_token
# def secret(token):
#     user = User.get_user_from_token(token)
#     return user.firstName


def get_info_from_google_id_token(id_token):
    """ Parses google id_token and returns user info
    :param id_token: token received from google
    :return: dict of user info
    """
    CLIENT_ID = app.config.get('CLIENT_ID')
    try:
        idinfo = client.verify_id_token(id_token, CLIENT_ID)
        if idinfo['aud'] not in [CLIENT_ID]:
            #raise crypt.AppIdentityError("Unrecognized client.")
            return False
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        # Invalid token
        return "Invalid token", 401
    except Exception:
        return False
    return idinfo


def check_user_exists(google_sub):
    """
    Check if the user exists
    :param google_sub: subject field from google data
    :return: user if exists else false
    """
    user = User.query.filter_by(google_sub=google_sub).first()
    if user is None:
        raise UserNotFound()
    else:
        return user

def generate_token(data):
    try:
        token = jwt.encode(data, key=app.config.get('SECRET_KEY'))
        return token
    except:
        raise InvalidUsage("Couldn't generate token. Retry")


def register_user(google_info):
    """
    Register user from the info from google
    :param google_info: Info got from google
    :return: registered user or None
    """
    email = google_info['email']
    firstName = google_info['given_name']
    lastName = google_info['family_name']
    google_sub = google_info['sub']
    try:
        user = User(email, firstName, lastName, google_sub)
        db.session.add(user)
        db.session.commit()
        return user
    except:
        raise UserCannotRegister()


def get_user_from_id(id):
    user = User.query.filter(User.id == id).first()
    if user is None:
        raise UserNotFound()
    else:
        return user