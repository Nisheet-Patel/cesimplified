from flask_login import UserMixin
from . import db

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.String(500))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title =  db.Column(db.String(200), nullable=False)
    topic = db.relationship('Topic', backref='course')

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title =  db.Column(db.String(250), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    videos = db.relationship('Videos', backref='course')

class Videos(db.Model):
    __searchable__ = ['title']
    vid = db.Column(db.String(20), primary_key=True)
    title =  db.Column(db.String(250), nullable=False)
    vtype = db.Column(db.String(20), nullable=False)
    topic_id  = db.Column(db.Integer, db.ForeignKey('topic.id'))