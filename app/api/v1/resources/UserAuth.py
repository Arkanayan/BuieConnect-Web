from flask_restful import Resource, reqparse
from app.auth import Auth
from .fields import LoginSchema, ErrorSchema, Error
from flask import request
from flask_restful import marshal


class UserAuth(Resource):
    """ Handles users authentication, login etc."""

    def __init__(self):
        # self.reqparse = reqparse.RequestParser(bundle_errors=True)
        pass

    def post(self):
        """
        Handles login function
        :return: auth token
        """
        # self.reqparse.add_argument('id_token', type=str, required=True,
        #                       help="No id_token provided", location='json')
        # data = self.reqparse.parse_args()
        # token = data['id_token']
        login_schema = LoginSchema(many=False)
        data, errors = login_schema.dump(request.json)
        print(data['id_token'])
        token = data['id_token']
        info = Auth.get_info_from_google_id_token(token)
        if info is False:
            error = {
                Error("Invalid id_token", code=401),
                Error("Invalid id_token", code=401)
            }
            error_schema = ErrorSchema()
            data = error_schema.dump(error, many=len(error))
            print(data)
            return data.data
        google_sub = info['sub']
        user = Auth.check_user_exists(google_sub)
        if user is not None:
            from flask import jsonify
            return jsonify({"token" : user.get_auth_token()})
        user = Auth.register_user(info)
        from .fields import user_fields
        return marshal(user, user_fields)
