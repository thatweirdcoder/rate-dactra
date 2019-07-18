import os

from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect

import forms
import models

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
models.db.init_app(app)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
csrf = CSRFProtect(app)


@app.before_first_request
def before_first_request():
    models.db.create_all()


@app.route('/', methods=('GET', 'POST'))
def index():
    form = forms.NewTeacherForm()
    if form.validate_on_submit():
        flash(f'{form.name.data}, ahhhhhhhhhhhhhh welcome!', 'info')  # TODO: put evil emoji here
        t = models.Teacher(name=form.name.data)
        models.db.session.add(t)
        models.db.session.commit()
        return redirect(url_for('index'))
    database = models.Teacher.query.order_by(models.Teacher.name).all()
    teachers = (
        {'name': t.name, 'photo': t.photo,
         'bedan_factor':
             f'{len([_ for _ in t.reviews if t.reviews.bedan]) / (len(t.reviews) if t.reviews else 1) * 100}%'}
        for t in database)
    context = {
        'form': form,
        'teachers': teachers
    }
    return render_template('index.html', **context)


@app.route('/<string:name>')
def teacher_page(name):
    context = {
        'name': name
    }
    return render_template('teacher_page.html', **context)


@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(_):
    return render_template('500.html')
