class BaseConfig(object):
    """Base config class"""
    SECRET_KEY = 'AasHy7I8484K8I32seu7nni8YHHu6786gi'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOADS_FOLDER = "application/database/media"
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


class ProductionConfig(BaseConfig):
    """Production specific config"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://samuelitwaru:password@localhost/traveler'  # TODO => MYSQL


class DevelopmentConfig(BaseConfig):
    """Development environment specific config"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/database.db'

