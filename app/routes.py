from flask import render_template, url_for, flash, redirect
from app.forms import LoginForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from app import app

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        user = current_user.username
    else:
        user = 'stranger'
    return render_template('index.html', title = 'Home', user = user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not form.password.data == user.password:
            flash(f'Invalid username or password!')
            return redirect(url_for('login'))
            # flash(f'Login requested for {form.username.data}')
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', title = 'Control Panel', users = User)