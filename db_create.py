# Database creation file
from app import db
from app.models import User, Role, Notice

# db.drop_all()
db.create_all()
role = Role(name="user", description="normal user without any privilege")
user = User("arka@created.com", "arcreated", "shit", "115917823430167122663", roles=role)
db.session.add(role)
db.session.add(user)
db.session.commit()
