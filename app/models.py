from datetime import datetime
from flask_login import UserMixin
from app import database, login
from sqlalchemy import and_

class TourParticipant(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    tour_id = database.Column(database.Integer, database.ForeignKey('tour.id'))
    tour_user_rating = database.Column(database.Float)
    tour_user_feedback = database.Column(database.String(128))

    #Initialise the values and add a custom property
    def __init__(self, current_tour, **kwargs):
        super(TourParticipant, self).__init__(**kwargs)
        # self.tour_id = current_tour
        # self._current_tour = current_tour
        # self.init_on_load()
        res = self.query.filter(self.tour_id == current_tour)
        self.__dict__ = res.__dict__


    # @database.reconstructor
    # def init_on_load(self):
        # self._current_tour = self._current_tour
        
    #Get current tour participants
    # @classmethod
    def get_participants(self):
        return self.query.filter(self.tour_id == self._current_tour)

    #Set feedback
    # @classmethod
    def set_feedback(self, feedback):
        # cls.tour_user_feedback = feedback
        participants = get_participants()
        participants.feedback = feedback
        database.session.commit()

    def join_tour(self, user_id):
        self.user_id = user_id
        self.tour_id = self._current_tour
        database.session.add(self)
        database.session.commit()

    
    # @classmethod
    def delete_participation(self):
        to_delete = has_participated()
        database.session.delete(to_delete)
        database.session.commit()

    # @classmethod
    def has_participated(self, tour_user_id, tour_participation = []):
        # tour_participation = self.query.filter(and_(self.user_id == tour_user_id, self.tour_id == self.current_tour)).all()
        tour_participation = self.query.filter(self.user_id == tour_user_id).first()
        print(tour_participation)
        return tour_participation

    #@classmethod
    # def get_participants(cls, tour_id, participants = []):
        # participants = cls.query.filter(cls.tour_id == tour_id).first()
        # return participants

    # @classmethod
    def get_all_feedback(self, feedback = []):
        feedback = self.query.filter(and_(self.tour_user_feedback != None, self.tour_id == self._current_tour)).all()
        return feedback


class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(32), index=True, unique=True)
    name = database.Column((database.String(64)))
    email = database.Column(database.String(50), index=True, unique=True)
    password = database.Column(database.String(128))
    tours = database.relationship('Tour', backref='author', lazy='dynamic')
    access = database.Column(database.String(10), default = '')
    description = database.Column(database.String(128))
    ratings  = database.Column(database.Float)
    f_status = database.Column(database.Integer)


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
    f_status = database.Column(database.Boolean)

    # @staticmethod
    # def is_owner(id):
        # return Tour.query.filter()

    @classmethod
    def get_tour(cls, id):
        return cls.query.get(id)
    @classmethod
    def get_tours(cls):
        return cls.query.filter(cls.f_status == None)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))