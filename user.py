from app import database
from app.models import User
import math, random


# Test script for users
for n in range(100+1):
    _n = str(n)
    username = f'callum_{_n}'
    password = '123456'
    email = f'callum{_n}@gmail.com'
    ratings = round(random.uniform(1, 5),1)


    _user = User(username = username, password = password,\
                email = email, ratings = ratings)
    database.session.add(_user)
    database.session.commit()