from flask_restful import Resource, reqparse


# Define articles resource api
class Articles(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No title provided', location='json')
        super(Articles, self).__init__()

    # articles GET request
    def get(self):
        return {'Articles': 'Hello article 1'}

    # trigger at POST request
    def post(self):
        data = self.reqparse.parse_args()
        return {"title": data['title']}

