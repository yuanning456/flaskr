import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:123456@127.0.0.1:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
