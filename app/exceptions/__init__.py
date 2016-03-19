from flask import jsonify
from marshmallow import pprint

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, errors=[]):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.errors = errors

    def to_dict(self):
        dict_errors = dict()
        dict_errors['errors'] = self.errors
        self.errors = dict(dict_errors)
        pprint(self.errors)
        rv = dict(self.errors or ())
        rv['message'] = self.message
        rv['code'] = self.status_code
        return rv


# User not found exception
class UserNotFound(InvalidUsage):
    def __init__(self, errors=None):
        self.message = "User not found"
        self.status_code = 404
        self.errors = []


class UserCannotRegister(InvalidUsage):
    def __init__(self):
        self.message = "Sorry, couldn't register user"
        self.status_code = 400
        self.errors = []


class ErrorNoToken(InvalidUsage):
    def __init__(self):
        self.message = "No token in header"
        self.status_code = 401
        self.errors = []


class ErrorNoIdToken(InvalidUsage):
    def __init__(self):
        self.message = "No id token provided. Make sure you have signed in with google."
        self.status_code = 401
        self.errors = []

class NotAuthorized(InvalidUsage):
    def __init__(self):
        self.message = "You are not authorized to access this resource"
        self.status_code = 403
        self.errors = []

class InvalidToken(InvalidUsage):
    def __init__(self):
        self.message = "Your auth token is invalid"
        self.status_code = 401
        self.errors = []

