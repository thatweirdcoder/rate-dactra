from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __table_name__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))  # TODO: fix this


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
