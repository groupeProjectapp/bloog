from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import re


from website.models import User

auth = Blueprint('auth', __name__)

def is_valid_password(password):
    min_length = 8
    uppercase_pattern = re.compile(r'[A-Z]')
    lowercase_pattern = re.compile(r'[a-z]')
    digit_pattern = re.compile(r'\d')
    special_char_pattern = re.compile(r'[!@#$%^&*()]')

    if len(password) < min_length:
        return False, "Password must be at least 8 characters long."
    if not uppercase_pattern.search(password):
        return False, "Password must contain at least one uppercase letter."
    if not lowercase_pattern.search(password):
        return False, "Password must contain at least one lowercase letter."
    if not digit_pattern.search(password):
        return False, "Password must contain at least one digit."
    if not special_char_pattern.search(password):
        return False, "Password must contain at least one special character (e.g., !@#$%^&*())."

    return True, "Password is valid."


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email='ENV_EMAIL'
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("your account sucessfully logged in!", "success")
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash("Login Faild", "error")
        else:
            flash("Login Faild", "error")
    return render_template("login.html",user=current_user)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name=request.form.get('name')
        email=request.form.get('email')
        password1=request.form.get('password1')
        password2=request.form.get('password2')



        if len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            valid, message = is_valid_password(password1)
            if not valid:
                flash(message, category='error')
            else:
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    flash('Email already exists.', category='error')
                else:
                    new_user = User(
                        email=email,
                        name=name,
                        password=generate_password_hash(password1, method="pbkdf2:sha1")
                    )
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect(url_for('views.index'))
    return render_template("register.html",user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))