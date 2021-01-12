import os

class BaseConfig(object):
    """Base config class"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SECRET_KEY = 'AasHy7I8484K8I32seu7nni8YHHu6786gi'
    TIMEZONE = "Africa/Kampala"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOADED_LOGOS_DEST = "app/models/media/"
    UPLOADED_LOGOS_URL = "app/models/media/"
    HOST_ADDRESS = "http://127.0.0.1:5000"
    # HOST_ADDRESS = "http://192.168.1.117:8000"
    # HOST_ADDRESS = "http://127.0.0.1:8000"
    # HOST_ADDRESS = "https://traveler-ug.herokuapp.com"
    DATETIME_FORMAT = "%B %d %Y, %I:%M %p %z"
    DATE_FORMAT = "%B %d %Y %z"
    DEFAULT_CURRENCY = "UGX"

    # local email
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'amobittechnologiez@gmail.com'
    MAIL_PASSWORD = '@_AmoBit2020'
    MAIL_PASSWORD = 'tydciogyjstlxpdt'
    MAIL_DEFAULT_SENDER = 'amobittechnologiez@gmail.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_SUPPRESS_SEND = False
    RAVE_PUBLIC_KEY = os.getenv("RAVE_PUBLIC_KEY")
    RAVE_SECRET_KEY = os.getenv("RAVE_SECRET_KEY")
    RAVE_ENCRYPTION_KEY = os.getenv("RAVE_ENCRYPTION_KEY")
    RAVE_TEST_NUMBER = "256752041475"
    RAVE_USING_ENV = False
    REDIS_CHAN = "booking"

    # send grid
    # MAIL_SERVER = 'smtp.sendgrid.net'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_DEFAULT_SENDER = 'samuelitwaru@gmail.com'
    # MAIL_USERNAME = 'apikey'
    # SENDGRID_API_KEY = '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'
    # SENDGRID_DEFAULT_FROM = 'samuelitwaru@gmail.com'
    

class ProductionConfig(BaseConfig):
    """Production specific config"""
    DEBUG = False
    TESTING = False
    HOST_ADDRESS = "https://traveler-ug.herokuapp.com"
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://samuelitwaru:password@localhost/traveler'  # TODO => MYSQL
    SQLALCHEMY_DATABASE_URI = 'sqlite:///models/database.db'
    RAVE_PRODUCTION = True
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')


class DevelopmentConfig(BaseConfig):
    """Development environment specific config"""
    DEBUG = True
    MAIL_DEBUG = True
    HOST_ADDRESS = "http://127.0.0.1:5000"
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:bratz123@localhost/traveler'  # TODO => MYSQL
    SQLALCHEMY_DATABASE_URI = 'sqlite:///models/database.db'
    RAVE_PRODUCTION = False
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')



