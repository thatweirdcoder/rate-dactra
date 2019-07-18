import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
db = SQLAlchemy(app)


class User(db.Model):
    __table_name__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))  # TODO: fix this


class Teacher(db.Model):
    __tabel_name__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(64), nullable=True)
    photo = db.Column(db.LargeBinary, nullable=True)


class Review(db.Model):
    __table_name__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    average_grading = db.Column(db.String(2))
    take_again = db.Column(db.Boolean)
    attendance = db.Column(db.Boolean)
    understanding = db.Column(db.Boolean)
    sexism = db.Column(db.Boolean)
    bedan = db.Column(db.Boolean)
    interesting = db.Column(db.Boolean)
    english = db.Column(db.Boolean)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship('Teacher', backref=db.backref('reviews', lazy=True))


class Comment(db.Model):
    __table_name__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(64))
    student_major = db.Column(db.String(64))
    grade_received = db.Column(db.String(2))
    comment = db.Column(db.String(140))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship('Teacher', backref=db.backref('comments', lazy=True))


@app.before_first_request
def before_first_request():
    db.create_all()


@app.route('/')
def index():
    context = {
        'teachers': Teacher.query.all()
    }
    return render_template('index.html', **context)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')
