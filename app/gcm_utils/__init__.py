from gcm import GCM
from app import app
from app.exceptions import CouldNotSendMessage
from app.models import Notice

gcm = GCM(app.config.get("GCM_API_KEY"))

def send_message(reg_ids, data):
    response = gcm.json_request(registration_ids=reg_ids,
                                data=data)
    return response["success"]


def send_to_all(data):
    topic = "global"
    try:
        response = gcm.send_topic_message(topic=topic, data=data)
        return response
    except:
        raise CouldNotSendMessage
