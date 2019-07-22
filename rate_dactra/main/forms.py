from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp


class NewTeacherForm(FlaskForm):
    name = StringField('Add a new teacher', validators=[
        DataRequired(), Length(max=42, min=2)
    ])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    name = StringField('Username', validators=[
        DataRequired(), Length(max=42, min=2),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Username must have only letters, numbers, dots or '
               'underscores')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(max=42, min=2)
    ])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Submit')
