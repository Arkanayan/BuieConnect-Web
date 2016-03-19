# Database creation file
from app import db
from app.models import User, Role, Notice, Dept

# db.drop_all()
db.create_all()
role = Role(name="user", description="normal user without any privileges")
admin_role = Role(name="admin", description="User with admin privileges")
cse_dept = Dept("CSE")
# user = User("arka@created.com", "arcreated", "shit", "115917823430167122663", roles=role)
db.session.add(role)
db.session.add(admin_role)
db.session.add(cse_dept)
# db.session.add(user)
db.session.commit()
