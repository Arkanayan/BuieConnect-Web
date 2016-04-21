import os
# Config Class
class Config(object):
    SECRET_KEY = 'secret'
    DATABASE_URI = 'sqlite:///:memory'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authorization"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    #SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_SALT = 'something_super_secret_change_in_production'
    CLIENT_ID = os.getenv("CLIENT_ID", None)
    GCM_API_KEY = os.getenv("GCM_API_KEY", None)
    FIREBASE_SECRET = os.getenv("FIREBASE_SECRET", None)

# config for testing purposes
class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = "postgresql://testuser:password@127.0.0.1:5432/buieconnect"
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_ECHO = True
    SERVER_NAME = "buieconnect.dev:5000"


# Config for used on production
class ProductionConfig(Config):
    TESTING = True
    DATABASE_URI = os.getenv("DATABASE_URI", None)
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_ECHO = False
