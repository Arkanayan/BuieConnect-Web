from app import db

db.session.close_all()
db.drop_all()