from flask import render_template, url_for, redirect, flash

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


@main.route('/<string:name>')
def teacher_page(name):
    context = {
        'name': name
    }
    return render_template('teacher_page.html', **context)
