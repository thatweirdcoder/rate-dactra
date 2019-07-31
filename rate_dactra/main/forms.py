from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, NoneOf


class NewTeacherForm(FlaskForm):
    name = StringField('Add a new teacher', validators=[
        DataRequired(),
        Length(max=42, min=2),
        NoneOf(['login', 'admin', 'compare'])
    ])
    submit = SubmitField('Submit')
