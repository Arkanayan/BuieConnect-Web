
from app import app, db
from app.models import User, Role
from flask import jsonify, request, g
import jwt
from app.exceptions import UserNotFound, UserCannotRegister, ErrorNoToken
from app.api.v1.resources.utils import get_users_json

from flask_restful import Resource
from marshmallow import pprint
from oauth2client import client, crypt


def require_login(func):
    from functools import wraps
    @wraps(func)
    def check_token(*args, **kwargs):
        # Check to see if it's in their session
        auth_token = get_token_from_header()
        try:
            user = get_user_from_token(auth_token)
        except UserNotFound:
          info = get_info_from_google_id_token(auth_token)
          try:
            #user = register_user(info)
            #json = get_users_json(user, False)
            #return jsonify, 201
            return jsonify(info)
          except:
            raise UserCannotRegister()
        print(auth_token)
        # Otherwise just send them where they wanted to go
        return func(*args, **kwargs)
    return check_token

def get_token_from_header():
    """
    Gets the token from the header
    :return: token
    """
    auth_token = request.headers.get('Authorization')
    if auth_token is None:
        raise ErrorNoToken()
    return auth_token

def require_admin(func):
    from functools import wraps
    @wraps(func)
    def check_admin(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if auth_token is None:
            return 'Access-denied', 401
        user = get_user_from_token(auth_token)
        if user is None:
            return 'Invalid token', 401
        if 'admin' in user.roles:
            return func(*args, **kwargs)
        else:
            return 'Access-denied', 401
    return check_admin


def get_user_from_token(token):
    """
    Get user object from the id_token
    :param token:
    :return user object or UserNotFound() error
    """
    try:
        user_string = jwt.decode(token, key=app.config.get('SECRET_KEY'))
    except:
        return None
    google_sub = user_string['google_sub']
    user = User.query.filter_by(google_sub=google_sub).first()
    if user is not None:
        g.user = user
        return user
    else:
        raise UserNotFound()


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
        idinfo = client._extract_id_token(id_token=id_token)
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
    return user if not None else False



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