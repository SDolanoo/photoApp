from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

view = Blueprint('view', __name__)

@view.route('/')
@login_required
def default_view():
    return redirect(url_for('view.index'))

@view.route('/documents')
@login_required
def index():
    print('currently logged in user', current_user)
    return render_template('index.html')




