import os

basedir = os.path.abspath(os.path.dirname(__file__))
DB_URI= "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username='root',
    password='lala123',
    hostname='localhost:3306',
    databasename='capacitaciones'
)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #   'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI= DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT= 465
    MAIL_USE_SSL= True
    MAIL_USERNAME = 'matiastorsello@gmail.com' 
    MAIL_PASSWORD = 'tslhruuhnnwmbslh'