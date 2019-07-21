from main import models
from . import main


@main.before_app_first_request
def before_first_request():
    models.db.create_all()
