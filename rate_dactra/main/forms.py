from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class NewTeacherForm(FlaskForm):
    name = StringField('Add a new teacher', [
        validators.length(max=42, min=2)
    ])
    submit = SubmitField('Submit')
