import os

class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_FOLDER = os.path.join(ROOT, 'static/upload/')


    USER = os.environ.get('POSTGRES_USER', 'seller')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', '123456')
    HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    PORT = os.environ.get('POSTGRES_PORT', '5432')
    DB = os.environ.get('POSTGRES_DB', 'shop')


    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = True