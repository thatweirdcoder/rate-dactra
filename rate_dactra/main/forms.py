from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, NoneOf

from .. import photos


class NewTeacherForm(FlaskForm):
    name = StringField('Add a new teacher', validators=[
        DataRequired(),
        Length(max=42, min=2),
        NoneOf(['login', 'admin', 'compare'])
    ])
    submit = SubmitField('Submit')


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
    phone = StringField('Teacher phone number (10XXXXXXXX) ', validators=[
        Length(min=10, max=13)
    ])
    submit = SubmitField('Edit')


class ReviewTeacherForm(FlaskForm):
    take_again = BooleanField('If you go back in time, would you take the class again?')
    attendance = BooleanField('Does the teacher care about attendance?')
    understanding = BooleanField('Do you understand from the teacher?')
    sexism = BooleanField('Does the teacher favour boys over girls or girls over boys? Sexist?')
    bedan = BooleanField('Bedan?')
    interesting = BooleanField('Is the teacher interesting?')
    english = BooleanField('Is the teacher good at English?')
    submit = SubmitField('Review')


class CommentOnTeacherForm(FlaskForm):
    course_name = StringField('Class name')
    grade_received = SelectField('Grade received',
                                 choices=list(enumerate(['A',
                                                         'B',
                                                         'C',
                                                         'D',
                                                         'F'])),
                                 validators=[
                                     DataRequired()
                                 ])
    comment = StringField('Comment', validators=[
        DataRequired
    ])
    submit = SubmitField('Comment')
