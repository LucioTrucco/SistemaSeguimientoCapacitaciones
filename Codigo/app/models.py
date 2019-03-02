from app import db, login,app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



Training_students = db.Table('training_students',
                             db.Column('training_id',
                                       db.Integer,
                                       db.ForeignKey('training.id')),
                             db.Column('student_id',
                                       db.Integer,
                                       db.ForeignKey('student.id'))
                             )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    trainings = db.relationship('Training', backref='trainer', lazy='dynamic')
    role = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    start = db.Column(db.DateTime())
    end = db.Column(db.DateTime())
    finalizada = db.Column(db.Boolean())
    description = db.Column(db.String(64))
    comments = db.Column(db.String(120))
    classes = db.relationship('Class', backref='training', lazy='dynamic')
    students = db.relationship('Student', secondary=Training_students,backref=db.backref('lstTraining', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Training {}>'.format(self.name)


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    date = db.Column(db.DateTime())
    topics = db.Column(db.String(64))
    topicsNext = db.Column(db.String(64))
    comments = db.Column(db.String(64))
    training_id = db.Column(db.Integer, db.ForeignKey('training.id'))
    def __repr__(self):
        return '<Class {}>'.format(self.topics)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    surname = db.Column(db.String(120))
    name = db.Column(db.String(120))
    degree = db.Column(db.String(120))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
