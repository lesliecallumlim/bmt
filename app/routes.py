from flask import render_template, url_for, flash, redirect, request
from app.forms import LoginForm, RegistrationForm, CreateTour, EditProfile
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
        tourparted = ''
    tour = Tour.query.all() 

    return render_template('index.html', title = 'Home', user = user, tours = tour)

@app.route('/joinedtours')
def joinedtours():
    tourparted = Tour.query.join(TourParticipant, (TourParticipant.tour_id == Tour.id)).filter(TourParticipant.user_id == current_user.id)
    tourcreated = Tour.query.filter(Tour.user_id == current_user.id)
    return render_template('joinedtour.html', title = 'Joined Tours',  tourcreated = tourcreated, tourpart = tourparted)

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
        flash('Deleted.', 'warning')
    return redirect(url_for('index'))

@app.route('/profile/<int:id>', methods = ['GET', 'POST'])
def profile(id):
    if current_user.is_authenticated:
        user = User.query.get(id)
        return render_template('profile.html', id = current_user.id, user = user)
    
    else:
        flash('You need to login or register first!', 'warning')
        return redirect(url_for('login'))


@app.route('/editprofile/<int:id>', methods = ['GET', 'POST'])
def editprofile(id):
    if not current_user.is_authenticated:
        flash('You need to login first!', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(id)
    form = EditProfile(curr_username = current_user.username, curr_email = current_user.email)

    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.name = form.name.data
        user.description = form.description.data
        database.session.commit()
        flash('Edited successfully.', 'success')

    elif request.method == 'GET':
        form.email.data = user.email
        form.username.data = user.username
        form.name.data = user.name
        form.description.data = user.description

    return render_template('editprofile.html', id = current_user.id, user = user, form = form)

    #else:
     #   flash('You need to login or register first!', 'warning')
      #  return redirect(url_for('login'))

@app.route('/viewtour/<int:id>', methods=['GET', 'POST'])
def viewtour(id):
    if current_user.is_authenticated:
        tour = Tour.query.get(id)   
        tour_owner = Tour.query.filter_by(user_id = current_user.id).first()
        tour_participation = TourParticipant.query.filter_by(tour_id=id).first()
    else:
        flash('You need to login or register first!', 'warning')
        return redirect(url_for('login'))
    return render_template('viewtour.html', title = 'View Tour', tour_owner = tour_owner, tour = tour, tour_participation = tour_participation)

@app.route('/jointour/<int:id>', methods = ['GET', 'POST'])
def jointour(id):
    tour = Tour.query.get(id)
    if not current_user.is_authenticated:
        flash('You need to login first!', 'warning')
        return redirect(url_for('login'))
    elif current_user.id == tour.user_id:
        flash('You cannot join your own tour!', 'warning')
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
        user = User(username = form.username.data, email = form.email.data,\
                    password = form.password.data, name = form.name.data,\
                    description = form.description.data)
        database.session.add(user)
        database.session.commit()
        flash('Congratulations, you are now registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if not current_user.is_authenticated:
        flash('You need to login first!', 'warning')
        return redirect(url_for('login'))
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

@app.route('/edittour/<int:id>', methods=['GET', 'POST'])
def edittour(id):
    if not current_user.is_authenticated:
        flash('You need to login first!', 'warning')
        return redirect(url_for('login'))
        
    tour = Tour.query.get(id)
    form = CreateTour()

    if form.validate_on_submit():
        tour.user_id = current_user.get_id()
        tour.tour_name=form.tour_name.data
        tour.tour_description = form.tour_description.data 
        tour.tour_location = form.tour_location.data
        tour.tour_price = form.tour_price.data
        tour.start_date = form.start_date.data
        tour.end_date = form.end_date.data
        database.session.commit()
        flash('Edited successfully.', 'success')

    elif request.method == 'GET':
        form.tour_name.data = tour.tour_name
        form.tour_description.data = tour.tour_description
        form.tour_location.data = tour.tour_location
        form.tour_price.data = tour.tour_price
        form.start_date.data = tour.start_date
        form.end_date.data = tour.end_date
    return render_template('edittour.html', id = id, form = form)


