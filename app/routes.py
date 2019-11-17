# Note that this route.py file essentially serve as a Controller between 
# the Boundary (the html pages under ./templates) and the Entity (models.py) 

from flask import render_template, url_for, flash, redirect, request
from app.forms import LoginForm, RegistrationForm, FeedbackForm, SearchForm, CreateTour, EditProfile
from app.models import User, Tour, TourParticipant, UserFeedback
from flask_login import current_user, login_user, logout_user, login_required
from app import app, database
from sqlalchemy import func, and_

# Index page
@app.route('/')
@app.route('/index')
def index():
    user = current_user.username if current_user.is_authenticated else 'stranger' 
    tour = Tour().get_tours()
    # Add pagination function, at 10 per page
    page = request.args.get('page', 1, type=int) 
    tour = tour.paginate(page, 10, False)
    next_url = url_for('index', page=tour.next_num) if tour.has_next else None
    prev_url = url_for('index', page=tour.prev_num) if tour.has_prev else None
    return render_template('index.html', user = user, tours = tour.items, next_url = next_url, prev_url = prev_url)

# Display list of joined tours
@app.route('/joinedtours')
def joinedtours():
    tourparted = User.get_participated_tours(user_id = current_user.id)
    tourcreated = User.get_created_tours(user_id = current_user.id)
    # Add pagination for created tours only
    page = request.args.get('page', 1, type=int) 
    tourcreated = tourcreated.paginate(page, 10, False)
    next_url = url_for('joinedtours', page=tourcreated.next_num) if tourcreated.has_next else None
    prev_url = url_for('joinedtours', page=tourcreated.prev_num) if tourcreated.has_prev else None
    return render_template('joinedtour.html',  tourcreated = tourcreated.items, tourpart = tourparted, next_url = next_url, prev_url = prev_url)

# Delete tour controller
@app.route('/deletetour/<int:id>', methods=['GET', 'POST'])
def deletetour(id):
    tour = Tour().get_tour(tour_id = id)
    tour.delete_tour(tour_user_id = current_user.id, access = current_user.access)
    flash('Deleted.', 'warning')
    return redirect(url_for('viewtour', id = id))

# Delete user controller
@app.route('/deleteuser/<int:id>', methods=['GET', 'POST'])
def deleteuser(id):
    user = User.get_user(user_id = id)
    if user.delete_user(access = current_user.access):
        flash('Deleted.', 'warning')
    else:
        flash('Unauthorised.', 'warning')
    return redirect(url_for('admin'))

# View profile
@app.route('/profile/<int:id>', methods = ['GET', 'POST'])
def profile(id):
    # If login-ed
    if current_user.is_authenticated:
        user = User.get_user(id)
        # Render feedback form
        form = FeedbackForm()

        # Get list of feedbacks
        user_feedback = UserFeedback().get_actual_feedback(target_user = id)

        # Let's check if the user had already provided a feedback, otherwise create a new record
        feedback = UserFeedback().has_feedback(target_user = id, by_user_id = current_user.id)
        if form.validate_on_submit():
            if feedback is None or feedback == []:
                feedback = UserFeedback(user_id = id, by_user_id = current_user.id,\
                                        user_feedback = form.tour_feedback.data)
                database.session.add(feedback)
                database.session.commit()
            else:
                feedback.set_user_feedback(form.tour_feedback.data)
            flash('Thank you for your feedback.', 'success')
            return redirect(url_for('profile', id = id))
                
        elif request.method == 'GET' and feedback is not None:
            form.tour_feedback.data = feedback.user_feedback
        return render_template('profile.html', user = user, form = form, feedback = feedback, user_feedbacks = user_feedback)
    else:
        flash('You need to login or register first!', 'warning')
        return redirect(url_for('login'))

# Edit profile
@app.route('/editprofile/<int:id>', methods = ['GET', 'POST'])
def editprofile(id):
    if not current_user.is_authenticated:
        flash('You need to login first!', 'warning')
        return redirect(url_for('login'))
    
    if current_user.id == id:
        user = User.get_user(id)

        form = EditProfile(curr_username = current_user.username, curr_email = current_user.email)

        if form.validate_on_submit():
            user.email = form.email.data
            user.username = form.username.data
            user.name = form.name.data
            user.description = form.description.data
            user.password = form.password.data
            database.session.commit()
            flash('Edited successfully.', 'success')

        # We just prepopulate the fields if it is a GET request, meaning users are
        # actually just viewing the edit page, and not posting it
        elif request.method == 'GET':
            form.email.data = user.email
            form.username.data = user.username
            form.name.data = user.name
            form.description.data = user.description
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('index'))

    return render_template('editprofile.html', id = current_user.id, user = user, form = form)

#View tour controller
@app.route('/viewtour/<int:id>', methods=['GET', 'POST'])
def viewtour(id):
    #Check for auth
    if current_user.is_authenticated:
        #Get the tour description
        tour = Tour().get_tour(tour_id = id) 
        
        #Get list of participants
        participants = TourParticipant().get_participants(tour_id = id)
        #Get usernames & email of participants
        user_joined_list = User.query.join(TourParticipant, (TourParticipant.user_id == User.id)).filter(TourParticipant.tour_id == id)
        tour_username = Tour().get_tour_owner(tour_id = id).username
        #Init form
        form = FeedbackForm()

        #Check if there are people init
        if participants is not None:
            tour_participation = TourParticipant().has_participated(tour_id = id, tour_user_id = current_user.id)
            feedback = TourParticipant().get_all_feedback(tour_id = id)
            #Set feedback, commit, and redirect if form is valid
            if form.validate_on_submit():
                tour_participation.set_feedback(form.tour_feedback.data)
                flash('Thank you for your feedback.', 'success')
                return redirect(url_for('viewtour', id = id))
            elif request.method == 'GET' and tour_participation is not None:
                form.tour_feedback.data = tour_participation.tour_user_feedback

        # Otherwise just return an empty list
        else:
            tour_participation = []
            feedback = []
    
    else:
        flash('You need to login or register first!', 'warning')
        return redirect(url_for('login'))

    
    return render_template('viewtour.html', title = 'View Tour',\
                                            tour_owner = tour.user_id,\
                                            form = form,\
                                            tour = tour,\
                                            tour_participation = tour_participation,\
                                            user_feedbacks = feedback,\
                                            user_joined_list = user_joined_list,\
                                            tour_username = tour_username)


@app.route('/jointour/<int:id>', methods = ['GET', 'POST'])
def jointour(id):
    tour = Tour.get_tour(tour_id = id)
    if not current_user.is_authenticated:
        flash('You need to login first!', 'warning')
        return redirect(url_for('login'))
    elif current_user.id == tour.user_id:
        flash('You cannot join your own tour!', 'warning')
    else:
        t = TourParticipant(user_id = current_user.id, tour_id = id)
        database.session.add(t)
        database.session.commit()
        flash('You joined the tour' , 'success')
    return redirect(url_for('viewtour', id = id))

# Rating
@app.route('/rate/<int:id>')
@app.route('/rate/<int:id>/<int:rating>', methods = ['GET', 'POST'])
def rate(id, rating):

    tour_part = TourParticipant().has_participated(tour_id = id, tour_user_id = current_user.id)
    tour = Tour.get_tour(tour_id = id)

    # Aggregate up all the previous tour ratings
    prev_tour_rating = TourParticipant().get_all_ratings(tour_id = id, tour_user_id = current_user.id)
    # Count all of the previous tour participants who rated except for the user
    tour_total_participant = TourParticipant().get_tour_user_count(tour_id = id, tour_user_id = current_user.id)
    # New user rating
    rating = float(rating)
    tour_part.set_tour_user_rating(new_rating = rating)
    # If it has not been already rated
    if tour_total_participant > 0:
        tour_ratings = float(prev_tour_rating.prev_rating+rating)/float(tour_total_participant+1)
        tour.set_tour_rating(new_rating = tour_ratings)
    else:
        tour.set_tour_rating(new_rating = rating)
    flash('Successfully rated!', 'success')
    return redirect(url_for('viewtour', id = id))

# Login handler
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

# Logout handler
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/leavetour/<int:id>/<int:user_id>', methods = ['GET', 'POST'])
def leavetour(id, user_id):
    leave = TourParticipant().has_participated(tour_id = id, tour_user_id = user_id)
    leave.delete_participation()
    flash('Deleted', 'warning')
    return redirect(url_for('viewtour', id = id, user_id = user_id))


# Admin page
@app.route('/admin')
@login_required
def admin():
    user = User().get_all_users()
    return render_template('admin.html', title = 'Control Panel', user = user)

# Registration
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

# Create Tours
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
    elif not form.validate_on_submit() and form.start_date.data is not None:
        flash('You need to enter a start date that is earlier than the end date!', 'danger')
    return render_template('create.html', title='Create Tour', form=form)

# Edit Tours
@app.route('/edittour/<int:id>', methods=['GET', 'POST'])
def edittour(id):
    if not current_user.is_authenticated:
        flash('You need to login first!', 'warning')
        return redirect(url_for('login'))
        
    tour = Tour.get_tour(tour_id = id)
    form = CreateTour()
    
    if request.method == 'GET':
        form.tour_name.data = tour.tour_name
        form.tour_description.data = tour.tour_description
        form.tour_location.data = tour.tour_location
        form.tour_price.data = tour.tour_price
        form.start_date.data = tour.start_date
        form.end_date.data = tour.end_date

    elif form.validate_on_submit():
        tour.user_id = current_user.get_id()
        tour.tour_name = form.tour_name.data
        tour.tour_description = form.tour_description.data 
        tour.tour_location = form.tour_location.data
        tour.tour_price = form.tour_price.data
        tour.start_date = form.start_date.data
        tour.end_date = form.end_date.data
        database.session.commit()
        flash('Edited successfully.', 'success')
        
    elif (not form.validate_on_submit()):
        flash('You need to enter a start date that is earlier than the end date!', 'danger')

    return render_template('edittour.html', id = id, form = form)


# Profile rating
@app.route('/rateprofile/<int:id>')
@app.route('/rateprofile/<int:id>/<int:rating>', methods = ['GET', 'POST'])
def rateprofile(id, rating):
    # tour_part = TourParticipant().has_participated(tour_id = id, tour_user_id = current_user.id)
    feedback = UserFeedback().get_feedback(target_user = id)
    has_feedback = UserFeedback().has_feedback(target_user = id, by_user_id = current_user.id)
    # Aggregate up all the previous user ratings
    prev_user_rating = UserFeedback().get_all_ratings(user_id = id, by_user_id = current_user.id)
    # Count all of the previous tour participants who rated except for the user
    total_user_rating_count = UserFeedback().get_user_rating_count(user_id = id, by_user_id = current_user.id)
    # New user rating
    rating = float(rating)
    # Get details of the user in question
    user = User.get_user(user_id = id)
    #Set rating
    if has_feedback == [] or has_feedback is None:
        user_feedback = UserFeedback(user_id = id, by_user_id = current_user.id, user_rating = rating)
        database.session.add(user_feedback)
        database.session.commit()
    else:
        has_feedback.set_user_rating(new_rating = rating)
    # If it has not been already rated
    if total_user_rating_count > 0:
        user_ratings = float(prev_user_rating.prev_rating+rating)/float(total_user_rating_count+1)
        user.set_user_rating(new_rating = user_ratings)
    else:
        user.set_user_rating(new_rating = rating)
    flash('Successfully rated!', 'success')
    return redirect(url_for('profile', id = id))


# Search 
@app.route('/search', methods = ['GET', 'POST'])
def search():
    form = SearchForm()
    search_string = form.search.data
    search_type = form.choice.data
    if search_type == 'Max Price':
        try:
            float(search_string)
        except:
            flash('Invalid input!', 'danger')
            return redirect(url_for('search'))
    if form.validate_on_submit():
        results = Tour.search_tour(string = search_string, type = search_type)
        page = request.args.get('page', 1, type=int) 
        results = results.paginate(page, 10, False)
        next_url = url_for('search', page=results.next_num) if results.has_next else None
        prev_url = url_for('search', page=results.prev_num) if results.has_prev else None
        return render_template('search.html', form = form,\
                                results = results.items, next_url = next_url, prev_url = prev_url)
    return render_template('search.html', form = form, results = [])