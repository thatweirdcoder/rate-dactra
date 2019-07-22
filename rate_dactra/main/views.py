from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required, login_user, logout_user

from . import main, forms, models


@main.route('/', methods=('GET', 'POST'))
def index():
    form = forms.NewTeacherForm()
    if form.validate_on_submit():
        flash(f'{form.name.data}, ahhhhhhhhhhhhhh welcome!', 'info')  # TODO: put evil emoji here
        t = models.Teacher(name=form.name.data)
        models.db.session.add(t)
        models.db.session.commit()
        return redirect(url_for('.index'))
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


@main.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    context = {
        'form': form
    }
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.name.data).first()
        if user and user.verity_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('.index')
            return redirect(next)
        flash('DUMBFUCK', 'error')
    return render_template('login.html', **context)


@main.route('/admin')
@login_required
def admin():
    context = {

    }
    return render_template('admin.html', **context)


@main.route('/logout')
def logout():
    context = {

    }
    logout_user()
    flash('Bye bye!', 'info')
    return redirect(url_for('.login', **context))

@main.route('/<string:name>')
def teacher_page(name):
    context = {
        'name': name
    }
    return render_template('teacher_page.html', **context)
