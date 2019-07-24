from flask import render_template, url_for, redirect, flash
from sqlalchemy.exc import IntegrityError

from . import main, forms
from .. import models
from .. import photos


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
            flash(f'{form.name.data.title()}, ahhhhhhhhhhhhhh welcome!', 'info')  # TODO: put evil emoji here
            return redirect(url_for('.index'))

    teachers = models.Teacher.query.order_by(models.Teacher.name).all()

    for teacher in teachers:
        teacher.bedan = f'{(len([r for r in teacher.reviews if r.bedan])) / (
            len(teacher.reviews) if teacher.reviews else 1) * 100}%'

    context = {
        'form': form,
        'teachers': teachers
    }
    return render_template('index.html', **context)


@main.route('/compare')
def compare():
    context = {

    }
    return render_template('compare.html', **context)


@main.route('/<string:name>', methods=['GET', 'POST'])
def teacher_page(name):
    teacher = models.Teacher.query.filter_by(name=name).first_or_404()
    form = forms.EditTeacherForm()
    if form.submit.data:
        if form.name.data:
            form.name.validate(form)
        if form.photo.data:
            form.photo.validate(form)
            filename = photos.save(form.photo.data)
            teacher.photo = photos.url(filename)
        if form.email.data:
            form.email.validate(form)
        if form.phone.data:
            form.phone.validate(form)

        models.db.session.add(teacher)
        models.db.session.commit()
        return redirect(url_for('.teacher_page', name=teacher.name))

    context = {
        'teacher': teacher,
        'form': form
    }
    return render_template('teacher_page.html', **context)
