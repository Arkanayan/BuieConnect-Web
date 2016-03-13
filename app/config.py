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

# config for testing purposes
class DevelopmentConfig(Config):
    DEBUG = True
    # DATABASE_URI = "postgresql://testuser:password@localhost:5432/buieConnect"
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URI
    SQLALCHEMY_ECHO = True


# Config for used on production
class ProductionConfig(Config):
    TESTING = True
