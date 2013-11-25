import os
from os.path import abspath, dirname, join

BASE_DIR = abspath(dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = "you-will-never-guess"

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = "postgresql://jcgrant:%2F%2FFyjb572nqpr1@localhost/food-site"
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

