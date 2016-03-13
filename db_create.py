# Database creation file
from app import db
from app.models import User, Role

# db.drop_all()
db.create_all()
role = Role(name="user", description="normal user without privilege")
user = User("arka@gmail.com", "arkanayan", "shit", "34234234", roles=role)
db.session.add(role)
db.session.add(user)
db.session.commit()
