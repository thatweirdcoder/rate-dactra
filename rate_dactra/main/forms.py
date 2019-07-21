from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class NewTeacherForm(FlaskForm):
    name = StringField('Add a new teacher', [
        validators.length(max=42, min=2)
    ])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    name = StringField('Username', [
        validators.length(max=42, min=2)
    ])
    password = PasswordField('Password', [
        validators.length(max=42, min=2)
    ])
    submit = SubmitField('Submit')
