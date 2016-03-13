
from app import app, db
from app.models import User, Role
from flask import jsonify, request
from flask.ext.login import LoginManager
from flask.ext.security import Security, login_required, SQLAlchemyUserDatastore
import jwt




def require_api_token(func):
    from functools import wraps
    @wraps(func)
    def check_token(*args, **kwargs):
        # Check to see if it's in their session
        auth_token = request.headers.get('Authorization')
        if auth_token is None:
            return 'Access-denied', 401
        print(auth_token)
        # Otherwise just send them where they wanted to go
        return func(auth_token, *args, **kwargs)

    return check_token


@app.route('/secret')
@require_api_token
def secret(token):
    user = User.get_user_from_token(token)
    return user.firstName

from oauth2client import  client, crypt


def get_info_from_google_id_token(id_token):
    """ Parses google id_token and returns user info
    :param id_token: token received from google
    :return: dict of user info
    """
    CLIENT_ID = app.config.get('CLIENT_ID')
    print(CLIENT_ID)
    try:
        idinfo = client._extract_id_token(id_token=id_token)

        if idinfo['aud'] not in [CLIENT_ID]:
             raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        # Invalid token
        print("invalid token")
        return "Invalid token", 401
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
    user = User(email, firstName, lastName, google_sub)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_from_id(id):
    user = User.query.get(id)
    return [user if not None else False]
