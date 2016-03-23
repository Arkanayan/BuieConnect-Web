from flask_restful import Resource
from marshmallow import ValidationError
from app import db
from flask import request
from app.api.v1.resources.fields import VerifyUserIds
from app.api.v1.resources.utils import get_users_json
from app.exceptions import OperationNotCompleted, InvalidInput
from app.models import User
class Verify(Resource):

    #@Auth.require_roles("admin", "user")
    def get(self):
        """
        This method returns verified users json unless ?verified=false is specified
        :return: verified users json else unverified users json
        """
        verified = request.args.get('verified')
        if verified is not None and str(verified).lower() == 'false':
            unverified_users = User.query.filter(User.verified == False).all()
            return get_users_json(unverified_users, True)

        verified_users = User.query.filter(User.verified == True).all()
        return get_users_json(verified_users, True)

    def post(self):
        verify_user_ids = VerifyUserIds(strict=True)

        try:
            result = VerifyUserIds(strict=True).load(request.json)
            ids = result.data['id']
            stmt = User.__table__.update().where(User.id.in_(ids)).values(verified=True)
            db.session.execute(stmt)
            db.session.commit()

        except ValidationError:
            raise InvalidInput
        except:
            raise OperationNotCompleted

        # print(result.data['id'])

        return result.data