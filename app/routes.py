from flask import render_template, url_for, flash, redirect
from app.forms import LoginForm, RegistrationForm, CreateTour
from app.models import User, Tour, TourParticipant
from flask_login import current_user, login_user, logout_user, login_required
from app import app, database

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        user = current_user.username
    else:
        user = 'stranger'

    tour = Tour.query.all()
    return render_template('index.html', title = 'Home', user = user, tours = tour)


@app.route('/deletetour/<int:id>', methods=['GET', 'POST'])
def deletetour(id):
    tour = Tour.query.get(id)
    if tour.user_id == current_user.id or current_user.access == 'admin':
        database.session.delete(tour)
        database.session.commit()
        flash('Deleted', 'warning')
    return redirect(url_for('index'))

@app.route('/deleteuser/<int:id>', methods=['GET', 'POST'])
def deleteuser(id):
    user = User.query.get(id)
    if current_user.access == 'admin':
        database.session.delete(user)
        database.session.commit()
        flash('Deleted', 'warning')
    return redirect(url_for('index'))

@app.route('/viewtour/<int:id>', methods=['GET', 'POST'])
def viewtour(id):
    tour = Tour.query.get(id)   
    tour_participation = TourParticipant.query.filter_by(tour_id=id).first()
    return render_template('viewtour.html', title = 'View Tour', tour = tour, tour_participation = tour_participation)

@app.route('/jointour/<int:id>', methods = ['GET', 'POST'])
def jointour(id):
    tour = Tour.query.get(id)
    if not current_user.is_authenticated:
        flash('You need to login first!', 'warning')
    elif current_user.id == tour.user_id:
        flash('You can''t join your own tour!')
    else:
        join = TourParticipant(user_id = current_user.id, tour_id = id)
        database.session.add(join)
        database.session.commit()
        flash('You joined the tour' , 'success')
    return redirect(url_for('viewtour', id = id))


@app.route('/leavetour/<int:id><int:user_id>', methods = ['GET', 'POST'])
def leavetour(id, user_id):
    tour = TourParticipant.query.filter_by(tour_id = id, user_id = user_id).first()
    database.session.delete(tour)
    database.session.commit()
    flash('Deleted', 'warning')
    return redirect(url_for('viewtour', id = id, user_id = user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not form.password.data == user.password:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login'))
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
    user = User.query.all()
    return render_template('admin.html', title = 'Control Panel', user = user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,\
                    password = form.password.data)
        database.session.add(user)
        database.session.commit()
        flash('Congratulations, you are now registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateTour()
    if form.validate_on_submit():
        tour_data = Tour(user_id = current_user.get_id(), tour_name=form.tour_name.data,\
                         tour_description = form.tour_description.data, tour_location = form.tour_location.data,\
                         tour_price = form.tour_price.data, start_date = form.start_date.data, \
                         end_date = form.end_date.data)
        database.session.add(tour_data)
        database.session.commit()
        flash('Congratulations, you have added a tour.', 'success')
        return redirect(url_for('create'))
    return render_template('create.html', title='Create Tour', form=form)