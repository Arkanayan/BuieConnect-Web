from flask.ext.restful import fields

notice_fields = {
    'title': fields.String,
    'message': fields.String,
    'url': fields.Url('apiv1.article')
}