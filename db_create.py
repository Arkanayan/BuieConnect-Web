# Database creation file
from app import db
from app.models import User, Role, Notice

# db.drop_all()
#db.create_all()
role = Role(name="user", description="normal user without any privileges")
admin_role = Role(name="admin", description="User with admin privileges")
super_admin = Role(name="superadmin", description="User with super admin privileges")
# cse_dept = Dept("CSE")
# user = User("arka@created.com", "arcreated", "shit", "115917823430167122633", roles=role)
db.session.add_all([role, admin_role, super_admin])
# db.session.add(user)
db.session.commit()
