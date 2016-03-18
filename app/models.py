from app import app, db
from flask.ext.login import UserMixin
from flask.ext.security import RoleMixin
from flask import jsonify
import jwt, datetime

# Define relationship
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


# Role model
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255), nullable=True)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    firstName = db.Column(db.String(255), default='')
    lastName = db.Column(db.String(255), default='')
    univ_roll = db.Column(db.Integer, nullable=True)
    google_sub = db.Column(db.String, unique=True)
    active = db.Column(db.Boolean, default=True)
    gcm_reg_id = db.Column(db.String, nullable=True)
    is_alumnus = db.Column(db.String, default=False)
    reg_date = db.Column(db.DateTime, default=datetime.datetime.now())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, firstName, lastName, google_sub, gcm_reg_id=None, roles=None):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.google_sub = google_sub
        self.gcm_reg_id = gcm_reg_id
        if roles is None:
            roles = Role.query.get(1)
        self.roles = [roles]

    def get_auth_token(self):
        """Generates user token
        :return: token
        """
        struct = {
            "id": self.id,
            "google_sub": self.google_sub,
            "email": self.email
        }
        token = jwt.encode(struct, key=app.config.get('SECRET_KEY'))
        return token

    # check if the user is admin or not
    def is_admin(self):
        admin_role = Role.query.filter_by(name='admin').first()
        return self.has_role(admin_role)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_google_sub(self):
        return self.google_sub


class Error:
    def __init__(self, message, code, errors=None):
        self.message = message
        self.code = code
        self.errors = errors





