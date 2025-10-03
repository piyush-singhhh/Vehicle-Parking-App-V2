import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "supersecretkey"

class LocalDevelopmentConfig(Config):
    DEBUG = True
    # Database inside instance folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'parking.db')
    SECRET_KEY = "vhdfjkhfghrifurwehfewfwemfnierwufh4iufhwefbwefbewilufgewi"
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = "sdjfhgksdhfglksdhfgklsdhfgklsdhfg"
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"


