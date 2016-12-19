class Config(object):
    DEBUG = False
    JSON_AS_ASCII = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:password@localhost:32773/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
