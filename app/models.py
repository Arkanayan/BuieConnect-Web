from app import app, db
from flask.ext.login import UserMixin
from flask.ext.security import RoleMixin
from flask import jsonify
import jwt, datetime
from pytz import timezone



def get_random_hash():
    """
    Generates random hash
    :return: hash
    """
    import random
    hash = random.getrandbits(128)
    return hash

kolkata_time_zone = timezone('Asia/Kolkata')

# Define relationship
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


# Role model
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.deferred(db.Column(db.String(255), nullable=True))

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<Role name: {}, description: {} >".format(self.name, self.description)


# User model
class User(db.Model):
    """
    User model
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    firstName = db.Column(db.String(255), default='')
    lastName = db.Column(db.String(255), default='')
    google_sub = db.Column(db.String, unique=True, index=True)
    verified = db.Column(db.Boolean, default=False)
    gcm_reg_id = db.deferred(db.Column(db.String, nullable=True))
    reg_date = db.deferred(db.Column(db.DateTime(kolkata_time_zone), default=datetime.datetime.now()))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    #notices = db.relationship('Notice', backref=db.backref('author', lazy='dynamic'))
    # Academic attributes
    is_alumnus = db.deferred(db.Column(db.Boolean, default=False), group='academic')
    univ_roll = db.deferred(db.Column(db.BigInteger, nullable=True), group='academic')
    admission_year = db.deferred(db.Column(db.SmallInteger), group='academic')
    current_semester = db.deferred(db.Column(db.SmallInteger), group='academic')
    passout_year = db.deferred(db.Column(db.SmallInteger), group='academic')
    department_name = db.deferred(db.Column(db.String))
    # token related attributes
    token_hash = db.deferred(db.Column(db.String))

    def __init__(self, email, firstName, lastName, google_sub, gcm_reg_id=None, roles=None):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.google_sub = google_sub
        self.gcm_reg_id = gcm_reg_id
        if roles is None:
            roles = Role.query.filter(Role.name == 'user').one()
        self.roles = [roles]
        self.token_hash = get_random_hash()

    def __repr__(self):
        return "<User fName: {}, lName: {}, email: {}, isAdmin: {} >".format(self.firstName, self.lastName, self.email,
                                                                             self.is_admin())

    def get_auth_token(self):
        """Generates user token
        :return: token
        """
        struct = {
            "id": self.id,
            "google_sub": self.google_sub,
            "token_hash": self.token_hash
        }
        token = jwt.encode(struct, key=app.config.get('SECRET_KEY'))
        return token

    def reset_token_hash(self):
        """
        Resets the token hash
        :return:
        """
        self.token_hash = get_random_hash()
        db.session.add(self)
        db.session.commit()

    # check if the user is admin or not
    def is_admin(self):
        """
        Check if the user is admin or not
        :return: true if admin else false
        """
        admin_role = Role.query.filter(Role.name.like("%admin%")).first()
        return admin_role in self.roles

    def is_superadmin(self):
        """
        Check if the user is super admin or not
        :return: true if super admin else false
        """
        superadmin_role = Role.query.filter(Role.name.like("%superadmin%")).first()
        return superadmin_role in self.roles

    def add_role(self, role):
        """
        Add role to current user
        :param role: role to add
        :return: true if succeed else false
        """
        try:
            self.roles.append(role)
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def set_verified(self, status):
        """
        Verify user
        commit to database after setting verification status
        :param status: status which the user will be changed to
        :return: true if verify succeed else false
        """
        try:
            self.verified = status
            return True
        except:
            return False

    def is_verified(self):
        return self.verified

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_google_sub(self):
        return self.google_sub


# Notice model
class Notice(db.Model):
    """
    Notice model
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    message = db.deferred(db.Column(db.String))
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", backref=db.backref('notices', lazy="dynamic"))

    def __init__(self, title, message=None, author=None):
        self.title = title
        self.message = message
        self.author = author

    def __repr__(self):
        return "<Notice title: {}, author: {}, date_created: {} >".format(self.title, self.author.name, self.date_created)


# Department model
# class Dept(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return "<Dept id: {}, name: {}".format(self.id, self.name)

# Error model
class Error:
    def __init__(self, message, code, errors=None):
        self.message = message
        self.code = code
        self.errors = errors


