from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Users
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("views.course"))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(username=username).first()

        # validators
        if not user:
            flash('Username Not Found !')
        elif not check_password_hash(user.password, password):
            flash("Password Incorrect !")
        else:
            login_user(user, remember=remember)
            return redirect(url_for('views.course'))

        return redirect(url_for('auth.login_page'))
    
    else:
        return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))