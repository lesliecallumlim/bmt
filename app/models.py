from datetime import datetime
from flask_login import UserMixin
from app import database, login

class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(32), index=True, unique=True)
    email = database.Column(database.String(50), index=True, unique=True)
    password = database.Column(database.String(128))
    tours = database.relationship('Tour', backref='author', lazy='dynamic')
    access = database.Column(database.String(10))

    def __repr__(self):
        return f'<User { self.username }>'


class Tour(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    tour_desc = database.Column(database.String(140))
    timestamp = database.Column(database.DateTime, index=True, default=datetime.now)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post {self.tour_desc}'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))