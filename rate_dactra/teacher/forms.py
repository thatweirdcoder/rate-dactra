from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, NoneOf

from rate_dactra import photos


class EditTeacherForm(FlaskForm):
    name = StringField('Teacher name', validators=[
        Length(max=42, min=2),
        NoneOf(['login', 'admin', 'compare'])
    ])
    photo = FileField('Teacher photo', validators=[
        FileAllowed(photos, 'Image only!')
    ])
    email = EmailField('Teacher email address', validators=[
        Email()
    ])
    phone = StringField('Teacher phone number', validators=[
        Length(min=10, max=13)
    ])
    submit = SubmitField('Edit')


class ReviewTeacherForm(FlaskForm):
    take_again = BooleanField('If you go back in time, would you take the class again?')
    attendance = BooleanField('Does the teacher care about attendance?')
    understanding = BooleanField('Do you understand from the teacher?')
    sexism = BooleanField('Does the teacher favour boys over girls or girls over boys? Sexist?')
    interesting = BooleanField('Is the teacher interesting?')
    english = BooleanField('Is the teacher good at English?')
    submit = SubmitField('Review')


class CommentOnTeacherForm(FlaskForm):
    course_name = StringField('Class name')
    grade_received = SelectField('Grade received',
                                 choices=(['A'] * 2,
                                          ['B'] * 2,
                                          ['C'] * 2,
                                          ['D'] * 2,
                                          ['F'] * 2),
                                 validators=[
                                     DataRequired()
                                 ])
    comment = StringField('Comment', validators=[
        DataRequired
    ])
    submit = SubmitField('Comment')
