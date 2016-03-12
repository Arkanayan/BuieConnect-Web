# Config Class
class Config(object):
    SECRET_KEY = 'secret'
    DATABASE_URI = 'sqlite://:memory'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI


# config for testing purposes
class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = "postgresql://testuser:password@localhost:5432/buieConnect"
    SQLALCHEMY_DATABASE_URI = DATABASE_URI


# Config for used on production
class ProductionConfig(Config):
    TESTING = True
