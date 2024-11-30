from datetime import timedelta
import re
from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for
from sqlalchemy.orm import Session

from .repository.user_repo import UserRepo
from .forms import LoginForm, SignupForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user

auth = Blueprint('auth', __name__)
session = Session(current_app.config['ENGINE'])

repo = UserRepo(session)

@auth.route('/signup')
def signup_get():
    return render_template('signup.html')

@auth.route('/login')
def login_get():
    print(current_app.config['ENGINE'])
    form = LoginForm()
    return render_template('login.html', form=form)

@auth.route('/signup', methods=['POST'])
def signup_post():
    form: SignupForm = SignupForm()

    validate_email(form.email.data)
    validate_username(form.username.data)
    validate_password(form.password.data)

    if form.validate_on_submit():

        user = repo.get_by_email(form.email.data)

        if user:
            if user.email == form.email.data:
                flash('Email already taken', 'email-error')
                return redirect(url_for('auth.signup_get'))
            if user.username == form.username.data:
                flash('Username already taken.', 'username-error')
                return redirect(url_for('auth.signup_get'))
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=form.email.data, username=form.username.data, password=generate_password_hash(form.password.data, method='pbkdf2:sha256'))

        # add the new user to the database
        repo.create(new_user)
        return redirect(url_for('auth.login_get'))
    flash('Invalid data', 'signup-error')
    return redirect(url_for('auth.signup_get'))

#works fine for now
@auth.route('/login', methods=['POST'])
def login_post():

    form: LoginForm = LoginForm()

    validate_email(form.email.data)
    validate_password(form.password.data)

    if form.validate_on_submit():
        
        user = repo.get_by_email(form.email.data)      
        #check if email exists
        if user is None:
            flash("Email does not exist", "email_error")
            return redirect(url_for('auth.login_get'))

        #email exists
        if not check_password_hash(user.password, form.password.data):
            flash("Invalid password", "password_error")
            return redirect(url_for('auth.login_get'))

        next = request.args.get('next')
        if form.remember.data == True:
            login_user(user, remember=True, duration=timedelta(days=5))
        else:
            login_user(user, duration=timedelta(hours=1))
        return redirect(url_for(next or 'view.index'))
    return redirect(url_for('auth.login_get'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_get'))


def validate_email(email: str):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        flash('Invalid email format', 'invalid_email')
        return redirect(url_for('auth.login_get'))
    
    
def validate_username(username: str):
    if len(username) < 8:
        flash('Username must be at least 8 characters long', 'short_username')
        return redirect(url_for('auth.login_get'))
    
    if not re.match(r'^[a-zA-Z0-9]+$', username):
        flash('Username cannot consist of special characters', 'special_username')
        return redirect(url_for('auth.login_get'))


def validate_password(password: str):
    if len(password) < 8:
        flash('Password must be at least 8 characters long', 'short_password')
        return redirect(url_for('auth.login_get'))

