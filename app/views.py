from app import app, db

from flask import json, request, jsonify
from .api.v1.resources.fields import UserUpdateSchema
from .api.v1.resources.utils import get_users_json

@app.route('/', methods=['POST'])
def index():
    # json_string = json.load(request.json)
    user_update_schema = UserUpdateSchema(partial=True)
    result = user_update_schema.load(request.json)
    db.session.add(result.data)
    db.session.commit()
    return jsonify({'roll': result.data.univ_roll})

