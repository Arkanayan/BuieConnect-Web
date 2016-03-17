from app import db, app
from app.models import Role,User
import jwt
from marshmallow import pprint
from app.api.v1.resources.fields import UserSchema

user = User.query.filter(User.id == 2).first()
user_schema = UserSchema()
data = user_schema.dump(user)
token = jwt.encode(data.data, key="secret")
pprint(token)
data = jwt.decode(token, key="secret")
pprint(data)