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

    def has_participated(self, tour_id, user_id):
        return self.query.filter(and_(self.tour_id == tour_id, self.user_id == user_id)).first()

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
    f_status = database.Column(database.Integer)

    def get_tour(self, id):
        return self.query.get(id)

    def get_tours(self):
        return self.query.filter(self.f_status == None)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))