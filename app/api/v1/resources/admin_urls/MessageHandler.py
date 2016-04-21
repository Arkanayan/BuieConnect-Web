from flask_restful import Resource
from marshmallow import ValidationError
from flask import request, g
from app.api.v1.resources.fields import MessagePayload, NoticeSchema
from app.exceptions import CouldNotSendMessage, InvalidInput
from app.gcm_utils import send_message, send_to_all
from app.models import User, Notice
from app import app
from app import db
from app import Auth
from app.Utils import Message
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
import time


# URL /admin/send
class MessageHandler(Resource):

    @Auth.require_admin
    def post(self):
        try:
            admin_user = g.get("user", None)
            payload = MessagePayload(strict=True).load(request.get_json())
            message_data = {
                    "title": payload.data.pop("title", ""),
                    "message": payload.data.pop("message", "")
                }
            message_type = payload.data.pop("type", Message.Type.notice.name)
            data = {
                "type" : message_type,
                "data" : message_data
            }
            # print(data)
            # token_generator = FirebaseTokenGenerator(app.config.get("FIREBASE_SECRET", None), admin=True)
            # auth_payload = { "appServer": True }
            # token = token_generator.create_token(auth_payload)
            auth = FirebaseAuthentication(app.config.get("FIREBASE_SECRET"), "app@email.com", admin=True)
            firebase_app = FirebaseApplication('https://buieconnect.firebaseio.com', auth)

            if "to" in payload.data:
                user_ids = payload.data['to']
                # load the users whose id matches and they are verified
                users = User.query.options(db.load_only("gcm_reg_id"))\
                    .filter(db.and_(User.id.in_(user_ids), User.verified==True)).all()

                reg_ids = [user.gcm_reg_id for user in users]
                response = send_message(reg_ids=reg_ids, data=data)
                return { "message_id": response,
                         "successful": True}

            elif "to_all" in payload.data:
                # send the data to all users
                response = send_to_all(data)
                # print("data: ", data)
                # print("response: ", response)
                # store notice to database
                notice = Notice(message_data["title"], message_data["message"], admin_user)
                db.session.add(notice)
                db.session.commit()
                notices_schema = NoticeSchema(many=False)
                result = notices_schema.dump(notice)
                result.data['.priority'] = 0 - int(time.time())
                from marshmallow import pprint
                #pprint(result.data)
                #firebase_result = firebase_app.post('/notices/{}'.format(result.data['id']), result.data, params={'print': 'pretty'},  headers={'X_FANCY_HEADER': 'VERY FANCY'})
                #firebase_result = firebase_app.put('/notices', result.data['id'], result.data, params={'print': 'pretty'} ,  headers={'X_FANCY_HEADER': 'VERY FANCY'})
                """
                Firebase notice format
                {
                    'id': 41,
                    'title': 'hi new title2',
                    'message': 'new message 1',
                    'url': 'http://buieconnect.dev:5000/api/v1/notices/41'
                }
                """
                firebase_app.put_async('/notices', result.data['id'], result.data, params={'print': 'silent'} ,  headers={'X_FANCY_HEADER': 'VERY FANCY'})
                #print(firebase_result)

                return { "message_id": response,
                         "successful": True}

            else:
                # For complex filter case e.g. with admission_year, passout_year
                payload.data['verified'] = True
                payload.data.pop("to", None)
                users = User.query.options(db.load_only("gcm_reg_id")).filter_by(**payload.data).all()
                reg_ids = [user.gcm_reg_id for user in users]
                response = send_message(reg_ids, data)

                return { "message_id": response,
                         "successful": True if response else False}

        except ValidationError:
            raise InvalidInput()
        except:
            raise CouldNotSendMessage

        # global
        # users = User.query.options(db.load_only("gcm_reg_id")).filter_by(verified=True).all()
