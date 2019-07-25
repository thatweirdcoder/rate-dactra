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
        teacher.bedan = f'''{
        (len([r for r in teacher.reviews if r.bedan])) / (len(teacher.reviews) if teacher.reviews else 1) * 100}%'''

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
    edit_teacher_form = forms.EditTeacherForm()
    if edit_teacher_form.submit.data:
        if edit_teacher_form.name.data:
            if edit_teacher_form.name.validate(edit_teacher_form):
                teacher.name = edit_teacher_form.name.data
                teacher.is_approved = False
                return redirect(url_for('.teacher_page', name=teacher.name))
        if edit_teacher_form.photo.data:
            if edit_teacher_form.photo.validate(edit_teacher_form):
                filename = photos.save(edit_teacher_form.photo.data)
                teacher.photo = photos.url(filename)
                teacher.is_approved = False
                return redirect(url_for('.teacher_page', name=teacher.name))
        if edit_teacher_form.email.data:
            if edit_teacher_form.email.validate(edit_teacher_form):
                teacher.email = edit_teacher_form.email.data
                teacher.is_approved = False
                return redirect(url_for('.teacher_page', name=teacher.name))
        if edit_teacher_form.phone.data:
            if edit_teacher_form.phone.validate(edit_teacher_form):
                teacher.phone = edit_teacher_form.phone.data
                teacher.is_approved = False
                return redirect(url_for('.teacher_page', name=teacher.name))

        models.db.session.add(teacher)
        models.db.session.commit()

    review_teacher_form = forms.ReviewTeacherForm()
    if review_teacher_form.validate_on_submit():
        review = models.Review(take_again=review_teacher_form.take_again.data,
                               attendance=review_teacher_form.attendance.data,
                               understanding=review_teacher_form.understanding.data,
                               sexism=review_teacher_form.sexism.data,
                               bedan=review_teacher_form.bedan.data,
                               interesting=review_teacher_form.interesting.data,
                               english=review_teacher_form.english.data,
                               teacher=teacher)
        models.db.session.add(review)
        models.db.session.commit()
        flash('Thank you for your review! You are Cute! :D', 'info')
        return redirect(url_for('.teacher_page', name=teacher.name))

    context = {
        'teacher': teacher,
        'edit_teacher_form': edit_teacher_form,
        'review_teacher_form': review_teacher_form
    }
    return render_template('teacher_page.html', **context)
