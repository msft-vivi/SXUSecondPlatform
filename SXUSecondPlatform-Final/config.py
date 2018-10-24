import os

MAX_CONTENT_LENGTH =16 * 1024 * 1024
UPLOAD_FOLDER = r'G:\Python\Project\SXUSecondPlatform\UpLoadFile\img\goods'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
DEBUG = True
# SECRET_KEY = os.urandom(24)
SECRET_KEY = 'ABC'
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD= '123'
#PASSWORD = '945151065.'
HOST = '127.0.0.1'
#HOST = '192.168.43.224'
#HOST = '39.105.89.107'
PORT = '3306'
#DATABASE = 'second_platform'
#DATABASE = 'book_onlinetest'
DATABASE = 'book_online'
#DATABASE = 'second_platform'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True

