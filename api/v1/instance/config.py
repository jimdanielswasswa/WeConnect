import os

SECRET_KEY = os.urandom(12)

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/weconnect'
