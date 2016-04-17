from flask_restful import Resource
from marshmallow import ValidationError
from flask import request, g
from app.api.v1.resources.fields import MessagePayload
from app.exceptions import CouldNotSendMessage, InvalidInput
from app.gcm_utils import send_message, send_to_all
from app.models import User, Notice
from app import db
from app import Auth
from app.Utils import Message

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
