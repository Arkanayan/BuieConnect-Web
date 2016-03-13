from flask_restful import Resource,reqparse, marshal_with
from .fields import notice_fields
from .fields import NoticeClass, NoticeSchema
from marshmallow import pprint
from flask import request
# Define single notice class
# Deals with single notice instances
class Notice(Resource):
    def __init__(self):
        pass

    # Returns a single article
    #@marshal_with(notice_fields, envelope="notice")
    def get(self, id):
        notice = {
            'title': 'This is title',
            'message': 'This is message ' + str(id),
            'id': id
        }
        noti = NoticeClass(2, 'this is title', 'this is message')
        schema = NoticeSchema()
        result = schema.dump(noti)
        pprint(result.data)
        return result.data

    # Put request, use to edit the article
    def put(self, id):
        request_data = request.json
        data, errors = NoticeSchema().load(request_data)
        print("data: ", data)
        print("errors: ", errors)
        return [data if len(errors) < 1 else errors]