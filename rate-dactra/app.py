import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from models import db, Teacher

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
db.init_app(app)


@app.before_first_request
def before_first_request():
    db.create_all()


@app.route('/')
def index():
    database = Teacher.query.all()
    teachers = ({'name': t.name, 'photo': t.photo,
                 'bedan_factor': f'{len([bf for bf in t.reviews if t.reviews.bedan])}/{len(t.reviews)}'}
                for t in database)
    context = {
        'teachers': teachers
    }
    return render_template('index.html', **context)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')
