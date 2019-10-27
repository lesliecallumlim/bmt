from app import database
from app.models import User, Tour

u = User(username='callum', email='callum@gmail.com', password = '123456', access = 'admin')

database.session.add(u)
database.session.commit()

u = User.query.all()

u