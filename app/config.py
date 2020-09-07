import os

class BaseConfig(object):
    """Base config class"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SECRET_KEY = 'AasHy7I8484K8I32seu7nni8YHHu6786gi'
    TIMEZONE = "UTC"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOADED_LOGOS_DEST = "app/models/media/"
    UPLOADED_LOGOS_URL = "app/models/media/"

class ProductionConfig(BaseConfig):
    """Production specific config"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://samuelitwaru:password@localhost/traveler'  # TODO => MYSQL
    


class DevelopmentConfig(BaseConfig):
    """Development environment specific config"""
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://samuelitwaru:password@localhost/traveler'  # TODO => MYSQL
    SQLALCHEMY_DATABASE_URI = 'sqlite:///models/database.db'

