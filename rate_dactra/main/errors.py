from flask import render_template

from . import main


@main.app_errorhandler(404)
def page_not_found(_):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(_):
    return render_template('500.html'), 500


@main.app_errorhandler(405)
def method_not_allowed(_):
    return render_template('405.html'), 405
