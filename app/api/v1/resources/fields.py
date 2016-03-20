from flask.ext.restful import fields
from app.models import User, Role, Error
from flask import g, url_for
from app.exceptions import NotAuthorized

notice_fields = {
    'title': fields.String,
    'message': fields.String,
    'url': fields.Url('apiv1.notice', absolute=True)
}

user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'firstName': fields.String,
    'lastName': fields.String,
    'univ_roll': fields.Integer,
    'google_sub': fields.String,
    'verified': fields.Boolean,
    'gcm_reg_id': fields.String,
    'is_alumnus': fields.Boolean,
    'reg_date': fields.DateTime,
    'url': fields.Url('apiv1.user', absolute=True)
}

token_fields = {
    'token': fields.String
}
from marshmallow import Schema, fields as filds, pre_load, post_load, post_dump
from app import marsh


class NoticeClass(object):
    def __init__(self, id, title, message):
        self.id = id
        self.title = title
        self.message = message


class BaseSchema(marsh.ModelSchema):
    __envelope__ = {
        'single': "key",
        'many': "keys"
    }

    __model__ = User

    def get_envelope_key(self, many):
        """Helper to get the envelope key."""
        key = self.__envelope__['many'] if many else self.__envelope__['single']
        assert key is not None, "Envelope key undefined"
        return key

    @pre_load(pass_many=True)
    def unwrap_envelope(self, data, many):
        key = self.get_envelope_key(many)
        return data[key]

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many):
        key = self.get_envelope_key(many)
        return {key: data}

    @post_load
    def make_object(self, data):
        return self.__model__(**data)


class NoticeSchema(Schema):
    id = filds.Integer()
    title = filds.String(required=True, error_messages={'required': 'Please enter a title.'})
    message = filds.String()
    url = filds.Method("notice_url", required=False)

    def notice_url(self, obj):
        return url_for('apiv1.notice', id=obj.id, _external=True)


class RoleSchema(marsh.ModelSchema):
    class Meta:
        model = Role


class UserSchema(marsh.ModelSchema):
    """
    Marshmallow schema for User model
    """
    __envelope__ = {
        'single': 'user',
        'many': 'users',
    }
    __model__ = User

    class Meta(BaseSchema.Meta):
        model = User
        exclude = ("notices", "roles", "department", "token_hash")

    roles = filds.Nested(RoleSchema, many=True, exclude=('id', 'description', 'users',))
    dept_name = filds.Method("department_name")
    # url = filds.Method('user_url')
    url = marsh.URLFor('apiv1.user', id='<id>', _external=True)

    def department_name(self, obj):
        return obj.department.name if obj.department is not None else None
        # def user_url(self, obj):
        #     return url_for('apiv1.user', id=obj.id, _external=True)


class LoginSchema(Schema):
    login_error_messages = {
        'required': 'Error: id_token is required for login',
    }
    id_token = filds.String(required=True, error_messages=login_error_messages)


class ErrorSchema(Schema):
    message = filds.String()
    code = filds.Integer()

    errors = filds.Nested('ErrorSchema', many=True, exclude=['errors'], dump_only=True)


class RegistraionDataSchema(Schema):
    id_token = filds.String(required=True)


class UserUpdateSchema(Schema):
    """
    This schema is matched with when user is updated
    """
    id = filds.Integer(required=True)
    email = filds.Email(required=False, allow_none=True)
    firstName = filds.String(required=False, allow_none=True)
    lastName = filds.String(required=False, allow_none=True)
    passout_year = filds.Int(required=False, allow_none=True)
    current_semester = filds.Integer(required=False, allow_none=True)
    is_alumnus = filds.Boolean(required=False, allow_none=True)
    univ_roll = filds.Integer(required=False, allow_none=True)
    admission_year = filds.Integer(required=False, allow_none=True)
    department_name = filds.String(required=False, allow_none=True)
    gcm_reg_id = filds.String(required=False, allow_none=True)

    @post_load
    def make_updated_user(self, data):
        # print(data)
        try:
            current_user = g.get('user', None)
            if current_user.id != data['id']:
                raise NotAuthorized
        except:
            raise NotAuthorized
        user = User.query.get(data['id'])
        del data['id']
        for key, value in data.items():
            if data[key] is not None and hasattr(user, key) and getattr(user, key) is not value:
                setattr(user, key, data[key])
        return user

class TokenDataSchema(Schema):
    """
    This schema fields is used to generate tokens
    """
    id = filds.Integer()
    google_sub = filds.String()
    token_hash = filds.String()