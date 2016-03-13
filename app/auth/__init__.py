
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

@app.route('/token')
def token():
    return User.query.filter_by(firstName='arka').first().get_auth_token()

@app.route('/log')
def log():
    user = User.query.first()
    role = user.roles[0]
    print("name: {} ; desc: {}".format(role.name, role.description))
    return str(user.get_auth_token())


@app.route('/dummy-api/', methods=['GET'])
def dummyAPI():
    ret_dict = {
        "Key1": "Value1",
        "Key2": "value2"
    }
    return jsonify(items=ret_dict)
