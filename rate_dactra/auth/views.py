from flask import request, url_for, flash, render_template, redirect
from flask_login import login_required, login_user, logout_user

from . import auth
from . import forms
from .. import models


@auth.route('/login', methods=('GET', 'POST'))
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
                next = url_for('.admin')
            return redirect(next)
        flash('DUMBFUCK', 'error')
    return render_template('login.html', **context)


@auth.route('/admin')
@login_required
def admin():
    context = {

    }
    return render_template('admin.html', **context)


@auth.route('/logout')
def logout():
    context = {

    }
    logout_user()
    flash('Bye bye!', 'info')
    return redirect(url_for('.login', **context))
