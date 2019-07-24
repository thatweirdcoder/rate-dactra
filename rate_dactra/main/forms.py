from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
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
    submit = SubmitField('Submit')

