from flask_wtf import FlaskForm
from wtforms import SubmitField


class ApproveForm(FlaskForm):
    approve = SubmitField('Approve')
    delete = SubmitField('Delete')
