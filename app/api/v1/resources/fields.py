from flask.ext.restful import fields
from app.models import User, Role


notice_fields = {
    'title': fields.String,
    'message': fields.String,
    'url': fields.Url('apiv1.notice', absolute=True)
}

user_fields = {
    'id' : fields.Integer,
    'email' : fields.String,
    'firstName' : fields.String,
    'lastName' : fields.String,
    'univ_roll' : fields.Integer,
    'google_sub' : fields.String,
    'active' : fields.Boolean,
    'gcm_reg_id' : fields.String,
    'is_alumnus' : fields.Boolean,
    'reg_date' : fields.DateTime,
    'url' : fields.Url('apiv1.user', absolute=True)
}
from marshmallow import Schema, fields as filds
from flask import url_for

class NoticeClass(object):
    def __init__(self, id, title, message):
        self.id = id
        self.title = title
        self.message = message



class NoticeSchema(Schema):
    id = filds.Integer()
    title = filds.String(required=True, error_messages={'required':'Please enter a title.'})
    message = filds.String()
    url = filds.Method("notice_url", required=False)

    def notice_url(self, obj):
        return url_for('apiv1.notice', id=obj.id, _external=True)

from marshmallow_sqlalchemy import ModelSchema


class RoleSchema(ModelSchema):
    class Meta:
        model = Role

class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ("active",)

    roles = filds.Nested(RoleSchema, many=True, exclude=('id','description','users',))
    url = filds.Method('user_url')

    def user_url(self, obj):
        return url_for('apiv1.user', id=obj.id, _external=True)




