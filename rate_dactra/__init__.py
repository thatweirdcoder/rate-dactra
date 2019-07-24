import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_uploads import configure_uploads, patch_request_class, UploadSet, IMAGES

from config import config
from .models import db, login_manager
from .navbars import nav

photos = UploadSet('photos', IMAGES)
bootstrap = Bootstrap()


def create_app(_):
    app = Flask(__name__)
    app.config.from_object(config[os.getenv('FLASK_CONFIG') or 'default'])

    bootstrap.init_app(app)
    db.init_app(app)
    nav.init_app(app)
    login_manager.init_app(app)
    configure_uploads(app, photos)
    patch_request_class(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
