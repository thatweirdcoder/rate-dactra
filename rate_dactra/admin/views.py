from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from rate_dactra import models
from . import admin, forms


@login_required
@admin.route('/admin')
def admin_home():
    teachers = models.Teacher.query.filter_by(is_approved=False).all()
    comments = models.Comment.query.filter_by(is_approved=False).all()
    approve_form = forms.ApproveForm()
    context = {
        'teachers': teachers,
        'comments': comments,
        'approve_form': approve_form
    }
    return render_template('admin.html', **context)


@login_required
@admin.route('/approve/<item_type>/<item>', methods=['POST'])
def approve(item_type, item):
    if item_type == 'teacher':
        item = models.Teacher.query.filter_by(id=item).first()
    elif item_type == 'comment':
        item = models.Comment.query.filter_by(id=item).first()
    approve_form = forms.ApproveForm()
    if approve_form.approve.data:
        item.is_approved = True
        models.db.session.add(item)
        models.db.session.commit()
        flash('approved')
        return redirect(url_for('.admin_home'))
    elif approve_form.delete.data:
        models.db.session.delete(item)
        models.db.session.commit()
        flash('deleted')
        return redirect(url_for('.admin_home'))
