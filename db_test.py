from app import db
from app.models import Role,User


user = User.query.filter(User.id == 2).first()
print('user' in user.roles)