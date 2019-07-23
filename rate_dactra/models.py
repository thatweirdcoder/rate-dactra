from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __table_name__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verity_password(self, password):
        return check_password_hash(self.password_hash, password)


class Teacher(db.Model):
    __table_name__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(64), nullable=True)
    photo = db.Column(db.LargeBinary, nullable=True)
    is_approved = db.Column(db.Boolean, default=False)


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
    is_approved = db.Column(db.Boolean, default=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship('Teacher', backref=db.backref('comments', lazy=True))
