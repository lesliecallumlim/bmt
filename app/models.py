from datetime import datetime
from flask_login import UserMixin
from app import database, login


class TourParticipant(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    tour_id = database.Column(database.Integer, database.ForeignKey('tour.id'))

    # def __repr__(self):
    #     return f'<Post {self.tour_desc}'


class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(32), index=True, unique=True)
    email = database.Column(database.String(50), index=True, unique=True)
    password = database.Column(database.String(128))
    tours = database.relationship('Tour', backref='author', lazy='dynamic')
    access = database.Column(database.String(10), default = '')

    # TourParticipant()

    # TourParticipated = database.relationship(
    #     'User', secondary = TourParticipant,
    #     primaryjoin = (TourParticipant.user_id == id),
    #     secondaryjoin = (TourParticipant.user_id == id),
    #     backref = database.backref('TourParticipant', lazy = 'dynamic'), lazy = 'dynamic')
    
    # def tour_followed(self):
    #     tours = Tour.query.join(
    #         TourParticipated, (TourParticipated.user_id == Tour.user_id)
    #         )
    #     own_tours = Tour.query.filter_by(user_id=self.id)
    #     return tours.union(own_tours)
        

    # def __repr__(self):
    #     return f'<User { self.username }>'


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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))