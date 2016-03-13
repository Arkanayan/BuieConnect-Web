from flask_restful import Resource, reqparse
from app.auth import get_info_from_google_id_token, check_user_exists, register_user

class UserAuth(Resource):
    """ Handles users authentication, login etc."""
    def post(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument('id_token', type=str, required=True,
                                   help="No id_token provided", location='json')
        data = self.reqparse.parse_args()
        token = data['id_token']
        info = get_info_from_google_id_token(token)
        google_sub = info['sub']
        user = check_user_exists(google_sub)
        if user is not None:
            return user.get_auth_token()
        user = register_user(info)
        return user.email
