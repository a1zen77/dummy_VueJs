class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True

    SECRET_KEY = "thisisasecretkey"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "thisisapasswordsalt"
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authorization-Token"
