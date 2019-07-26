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
            flash(f'{form.name.data.title()}, ahhhhhhhhhhhhhh welcome! :D', 'info')  # TODO: put evil emoji here
            return redirect(url_for('.index'))

    teachers = models.Teacher.query.order_by(models.Teacher.name).all()

    for teacher in teachers:
        teacher.bedan = f'''{
        (len([r for r in teacher.reviews if r.bedan])) // ((len(teacher.reviews) if teacher.reviews else 1) / 100)}%'''

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
    comments = models.Comment.query.filter_by(teacher=teacher).all()
    edit_teacher_form = forms.EditTeacherForm()
    review_teacher_form = forms.ReviewTeacherForm()
    comment_on_teacher_form = forms.CommentOnTeacherForm()

    reviews_num = (len(teacher.reviews) if teacher.reviews else 1) / 100
    teacher.take_again = (len([r for r in teacher.reviews if r.take_again])) // reviews_num
    teacher.attendance = (len([r for r in teacher.reviews if r.attendance])) // reviews_num
    teacher.understanding = (len([r for r in teacher.reviews if r.understanding])) // reviews_num
    teacher.sexism = (len([r for r in teacher.reviews if r.sexism])) // reviews_num
    teacher.bedan = (len([r for r in teacher.reviews if r.bedan])) // reviews_num
    teacher.interesting = (len([r for r in teacher.reviews if r.interesting])) // reviews_num
    teacher.english = (len([r for r in teacher.reviews if r.english])) // reviews_num

    over_all = (teacher.take_again, teacher.attendance, teacher.understanding, teacher.sexism, teacher.bedan,
                teacher.interesting, teacher.english)
    teacher.overall = sum(over_all) // len(over_all)

    context = {
        'teacher': teacher,
        'comments': comments,
        'edit_teacher_form': edit_teacher_form,
        'review_teacher_form': review_teacher_form,
        'comment_on_teacher_form': comment_on_teacher_form
    }
    return render_template('teacher_page.html', **context)


@main.route('/edit/<string:name>', methods=['POST'])
def edit_teacher(name):
    teacher = models.Teacher.query.filter_by(name=name).first_or_404()
    edit_teacher_form = forms.EditTeacherForm()
    if edit_teacher_form.name.data:
        if edit_teacher_form.name.validate(edit_teacher_form):
            teacher.name = edit_teacher_form.name.data.lower()
            teacher.is_approved = False
            flash(f'Name changed to {teacher.name.title()}')
    if edit_teacher_form.photo.data:
        if edit_teacher_form.photo.validate(edit_teacher_form):
            filename = photos.save(edit_teacher_form.photo.data)
            teacher.photo = photos.url(filename)
            teacher.is_approved = False
            flash(f'Photo changed to .. You can see it down below!')
    if edit_teacher_form.email.data:
        if edit_teacher_form.email.validate(edit_teacher_form):
            teacher.email = edit_teacher_form.email.data
            teacher.is_approved = False
            flash(f'Email changed to {teacher.email}')
    if edit_teacher_form.phone.data:
        if edit_teacher_form.phone.validate(edit_teacher_form):
            teacher.phone = edit_teacher_form.phone.data
            teacher.is_approved = False
            flash(f'Phone changed to {teacher.phone}')

    models.db.session.add(teacher)
    models.db.session.commit()
    return redirect(url_for('.teacher_page', name=name))


@main.route('/review/<string:name>', methods=['POST'])
def review_teacher(name):
    teacher = models.Teacher.query.filter_by(name=name).first_or_404()
    review_teacher_form = forms.ReviewTeacherForm()
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
    return redirect(url_for('.teacher_page', name=name))


@main.route('/comment/<string:name>', methods=['POST'])
def comment_on_teacher(name):
    teacher = models.Teacher.query.filter_by(name=name).first_or_404()
    comment_on_teacher_form = forms.CommentOnTeacherForm()
    comment = models.Comment(course_name=comment_on_teacher_form.course_name.data,
                             grade_received=comment_on_teacher_form.grade_received.data,
                             comment=comment_on_teacher_form.comment.data,
                             teacher=teacher)
    models.db.session.add(comment)
    models.db.session.commit()
    flash('Than you for your comment! You are Cute! :D')
    return redirect(url_for('.teacher_page', name=name))
