from flask_restful import Resource,reqparse, marshal_with
from .fields import notice_fields


# Define single notice class
# Deals with single notice instances
class Notice(Resource):
    def __init__(self):
        pass

    # Returns a single article
    @marshal_with(notice_fields, envelope="notice")
    def get(self, id):
        notice = {
            'title': 'This is title',
            'message': 'This is message ' + str(id),
            'id': id
        }
        return notice

    # Put request, use to edit the article
    def put(self, id):
        return { 'put': 'this is put of article of id ' + str(id)}