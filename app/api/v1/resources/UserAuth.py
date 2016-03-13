from flask_restful import Resource, reqparse
from app.auth import Auth


class UserAuth(Resource):
    """ Handles users authentication, login etc."""

    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)

    def post(self):
        """
        Handles login function
        :return: auth token
        """
        self.reqparse.add_argument('id_token', type=str, required=True,
                                   help="No id_token provided", location='json')
        data = self.reqparse.parse_args()
        token = data['id_token']
        info = Auth.get_info_from_google_id_token(token)
        google_sub = info['sub']
        user = Auth.check_user_exists(google_sub)
        if user is not None:
            return user.get_auth_token()
        user = Auth.register_user(info)
        return user.email
