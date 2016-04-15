from flask_restful import Resource, reqparse
from flask_marshmallow import pprint

# Define articles resource api
from app.api.v1.resources.fields import NoticeSchema
from app.exceptions import NoticeNotFound
from app.models import Notice


class NoticeList(Resource):
    def __init__(self):

        super(NoticeList, self).__init__()

    # articles GET request
    def get(self, id=None):
        if id is None:
            notice_schema = NoticeSchema(many=True)
            notices = Notice.query.order_by(Notice.id.desc()).limit(10)
            result = notice_schema.dump(notices)
            return result.data
        else:
            notice = Notice.query.get(id)
            if notice is None:
                raise NoticeNotFound
            else:
                notice_schema = NoticeSchema(many=False)
                result = notice_schema.dump(notice)
                return result.data


    # # trigger at POST request
    # def post(self):
    #     self.reqparse = reqparse.RequestParser()
    #     self.reqparse.add_argument('title', type=str, required=True,
    #                                help='No title provided', location='json')
    #     data = self.reqparse.parse_args()
    #     req_data =[]
    #     req_data.append(data)
    #     pprint(req_data)
    #     return req_data
    #
    # def patch(self):
    #     list = []
    #     final_dict = { 'message' : 'this is the message'}
    #     second_dict = { 'error': 'error1'}
    #     third_dict = { 'error': 'error2'}
    #     list.append(second_dict)
    #     list.append(third_dict)
    #     final_dict['errors'] = list
    #     pprint(final_dict)
    #     return final_dict

