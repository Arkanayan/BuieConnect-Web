from flask.ext.restful import fields

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