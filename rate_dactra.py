import os

from flask_migrate import Migrate

from main.models import User, Teacher, Review, Comment
from rate_dactra import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Teacher=Teacher, Review=Review, Comment=Comment)
