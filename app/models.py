from datetime import datetime
from flask_login import UserMixin
from app import database, login
from sqlalchemy import and_, or_, false, true, func

# This is the TourParticipation class
class TourParticipant(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    tour_id = database.Column(database.Integer, database.ForeignKey('tour.id'))
    tour_user_rating = database.Column(database.Float)
    tour_user_feedback = database.Column(database.String(128))

    def join_tour(user_id, tour_id):
        join = TourParticipant(tour_id = tour_id, user_id = user_id)
        database.session.add(join)
        database.session.commit()
        
    # Modifies the record in the database itself
    def set_feedback(self, feedback):
        self.tour_user_feedback = feedback
        database.session.commit()
    
    # Deletes the record in the database itself
    def delete_participation(self):
        database.session.delete(self)
        database.session.commit()

    def set_tour_user_rating(self, new_rating):
        if self.tour_user_rating != new_rating:
            self.tour_user_rating = new_rating
            database.session.commit() 

    # Returns a list of participants of a tour
    @staticmethod
    def get_participants(tour_id, participants = None):
        participants = TourParticipant.query.filter(TourParticipant.tour_id == tour_id)
        return participants

    # Returns a mutable object which can be used to modify the object state
    # More specifically, returns a record if the user has participated in the tour  
    @classmethod
    def has_participated(cls, tour_id, tour_user_id, tour_participation = []):
        tour_participation = cls.query.filter(and_(cls.tour_id == tour_id, cls.user_id == tour_user_id)).first()
        return tour_participation


    # Gets a list of feedback of a tour 
    @staticmethod
    def get_all_feedback(tour_id, feedback = []):
        feedback = TourParticipant.query.filter(and_(TourParticipant.tour_id == tour_id, TourParticipant.tour_user_feedback != None)).all()
        return feedback
    
    # Get sum of all ratings
    @staticmethod
    def get_all_ratings(tour_id, tour_user_id, rating = None):
        rating = TourParticipant.query.with_entities(func.sum(TourParticipant.tour_user_rating).label('prev_rating'))\
                    .filter(and_(TourParticipant.tour_id == tour_id, TourParticipant.user_id != tour_user_id)).first()
        return rating
    
    # Get list of users who rated
    @staticmethod
    def get_tour_user_count(tour_id, tour_user_id, count = None):
        count = TourParticipant.query.filter(and_(TourParticipant.tour_id == tour_id, TourParticipant.user_id != tour_user_id,\
                TourParticipant.tour_user_rating.isnot(None))).count()
        return count

class UserFeedback(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    user_id =  database.Column(database.Integer, database.ForeignKey('user.id'))
    user_rating = database.Column(database.Float)
    user_feedback = database.Column(database.String(128))
    by_user_id = database.Column(database.Integer)

    # Get all feedback inclusive of ratings
    @classmethod
    def get_feedback(cls, target_user):
        feedback = cls.query.filter(cls.user_id == target_user)
        return feedback
    
    @classmethod
    def get_actual_feedback(cls, target_user, feedback = []):
        feedback = cls.query.filter(and_(cls.user_id == target_user, cls.user_feedback.isnot(None)))
        return feedback

    # Get all ratings
    @staticmethod
    def get_all_ratings(user_id, by_user_id, ratings = None):        
        rating = UserFeedback.query.with_entities(func.sum(UserFeedback.user_rating).label('prev_rating'))\
                    .filter(and_(UserFeedback.user_id == user_id, UserFeedback.by_user_id != by_user_id)).first()
        return rating

    # Get list of users who rated
    @staticmethod
    def get_user_rating_count(user_id, by_user_id, count = None):
        count = UserFeedback.query.filter(and_(UserFeedback.user_id == user_id,\
                UserFeedback.user_rating != None, UserFeedback.by_user_id != by_user_id)).count()
        return count

    # Check if there is a feedback
    @classmethod
    def has_feedback(cls, target_user, by_user_id, feedback = None):
        feedback = cls.query.filter(and_(cls.user_id == target_user, cls.by_user_id == by_user_id)).first()
        return feedback

    # Set user rating
    def set_user_rating(self, new_rating):
        if self.user_rating != new_rating:
            self.user_rating = new_rating
            database.session.commit() 

    # Set feedback
    def set_user_feedback(self, feedback):
        self.user_feedback = feedback
        database.session.commit()
    
    

class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(32), index=True, unique=True)
    name = database.Column((database.String(64)))
    email = database.Column(database.String(50), index=True, unique=True)
    password = database.Column(database.String(128))
    access = database.Column(database.String(10), default = '')
    description = database.Column(database.String(128))
    f_status = database.Column(database.Boolean, default = False)
    ratings = database.Column(database.Float)

    # Return user
    @classmethod
    def get_user(cls, user_id):
        return cls.query.get(user_id)
    
    # Return users
    @classmethod
    def get_all_users(cls, user_list = []):
        user_list = cls.query.all()
        return user_list

    # Delete user: we technically don't delete the user but rather,
    # we just stop displaying it in the user list across
    def delete_user(self, access):
        # Only admins can delete  
        if access == 'admin':
            self.f_status = True
            database.session.commit()
            return True
        else:
            return False

    def set_user_rating(self, new_rating):
        self.ratings = new_rating
        database.session.commit()


    # Returns a list of participated tours that are not deleted.
    @staticmethod
    def get_participated_tours(user_id, tour_participated = []):
        tour_participated = Tour.query.join(TourParticipant, (TourParticipant.tour_id == Tour.id)).filter(and_(TourParticipant.user_id == user_id, Tour.f_status != True))
        return tour_participated
        
    # Returns a list of created tours that are not deleted.
    @staticmethod
    def get_created_tours(user_id, tour_participated = []):
        tour_created = Tour.query.filter(and_(Tour.user_id == user_id, Tour.f_status != True))
        return tour_created

    

class Tour(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    tour_name = database.Column(database.String(50))
    tour_description = database.Column(database.String(140))
    tour_location = database.Column(database.String(50))
    tour_price = database.Column(database.Float)
    start_date = database.Column(database.DateTime)
    end_date = database.Column(database.DateTime)
    timestamp = database.Column(database.DateTime, index=True, default=datetime.now)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    ratings  = database.Column(database.Float)
    f_status = database.Column(database.Boolean, default = False)

    @staticmethod
    def get_tour_owner(tour_id):
        return User.query.join(Tour, (Tour.user_id == User.id)).filter(Tour.id == tour_id).first()

    # Delete tour: we technically don't delete the tour but rather,
    # we just stop displaying it in the tour list across
    def delete_tour(self, tour_user_id, access):
        # Only admins and tour creator can delete the tours 
        if self.user_id == tour_user_id or access == 'admin':
            self.f_status = True
            database.session.commit()

    # Set the rating
    def set_tour_rating(self, new_rating):
        self.ratings = new_rating
        database.session.commit()

    # Returns a tour
    @classmethod
    def get_tour(cls, tour_id, tour_list = []):
        tour_list = cls.query.get(tour_id)
        return tour_list

    # Returns a list of tours
    @staticmethod
    def get_tours(tour_list = []):
        tour_list = Tour.query.filter(Tour.f_status != True)
        return tour_list

    # Search
    @staticmethod
    def search_tour(string, type, tour_list = []):
        _string = "%{}%".format(string)
        if type == 'Tour Name':
            tour_list = Tour.query.filter(Tour.tour_name.like(_string))
        elif type == 'Location':
            tour_list = Tour.query.filter(Tour.tour_location.like(_string))
        elif type == 'Max Price':
            tour_list = Tour.query.filter(Tour.tour_price <= float(string))
        return tour_list


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# class DBHandler(BaseQuery):
