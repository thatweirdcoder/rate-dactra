from flask import render_template, url_for, redirect, flash
from sqlalchemy.exc import IntegrityError

from . import main, forms
from .. import models


@main.route('/', methods=('GET', 'POST'))
def index():
    form = forms.NewTeacherForm()
    if form.validate_on_submit() and form.name.data not in ('login', 'admin', 'compare'):
        t = models.Teacher(name=form.name.data.lower().strip())
        try:
            models.db.session.add(t)
            models.db.session.commit()
        except IntegrityError:
            flash('Already in the database!', 'error')
            models.db.session.rollback()
        else:
            flash(f'{form.name.data.title()}, ahhhhhhhhhhhhhh welcome! :D', 'info')  # TODO: put evil emoji here
            return redirect(url_for('.index'))

    teachers = models.Teacher.query.order_by(models.Teacher.name).all()


    context = {
        'form': form,
        'teachers': teachers
    }
    return render_template('main/index.html', **context)
