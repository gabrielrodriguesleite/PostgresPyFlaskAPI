import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        'postgresql://carford_user:carford_password@db:5432/carford_db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
