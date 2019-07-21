from flask import Flask
from flask_bootstrap import Bootstrap

from config import config
from main.models import db
from main.navbars import nav

bootstrap = Bootstrap()


def create_app(c):
    app = Flask(__name__)
    app.config.from_object(config['development'])  # TODO: fix this error with flask cli

    bootstrap.init_app(app)
    db.init_app(app)
    nav.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
