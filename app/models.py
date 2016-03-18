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
    #notices = db.relationship('Notice', backref=db.backref('author', lazy='dynamic'))

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


# Notice model
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    message = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", backref=db.backref('notices', lazy="dynamic"))

    def __init__(self, title, message=None, author=None):
        self.title = title
        self.message = message
        self.author = author


# Department model
class Dept(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name


# Academic info model
class Academic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('academic', lazy="dynamic"))
    admission_year = db.Column(db.SmallInteger)
    current_semester = db.Column(db.SmallInteger)
    passout_year = db.Column(db.SmallInteger)
    dept_id = db.Column(db.Integer, db.ForeignKey('dept.id'))
    department = db.relationship('Dept', backref=db.backref('academics', lazy='dynamic'))

    def __init__(self, user, admission_year, current_sem, passout_year, department):
        self.user = user
        self.admission_year = admission_year
        self.current_semester = current_sem
        self.passout_year = passout_year
        self.department = department


class Error:
    def __init__(self, message, code, errors=None):
        self.message = message
        self.code = code
        self.errors = errors





