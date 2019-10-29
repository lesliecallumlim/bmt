from app import database
from app.models import User, Tour
import math, random
from datetime import date
countries = ['China', 'Singapore', 'Malaysia', 'Cambodia', 'Australia', 'Japan', 'New Zealand', 'Indonesia']
tour = ['Explore', 'Enjoy', 'Experience']


for n in range(20+1):
    tour_location = countries[random.randrange(len(countries))]
    tour_name = tour[random.randrange(len(tour))] + ' ' + country
    tour_description = 'Enjoy a fun-filled adventure in ' + country + '! Bringing you highlight reel of the country! '
    tour_price = random.randrange(100)
    lower_bound = date.today().toordinal()
    upper_bound = date.today().replace(day=31, month=12).toordinal()
    start_date = date.fromordinal(random.randint(lower_bound, upper_bound))
    end_date = date.fromordinal(random.randint(start_date.toordinal(), upper_bound))
    ratings = random.uniform(1, 5)

    tour = Tour(user_id = 1, tour_location = tour_location, tour_name = tour_name\
                tour_description = tour_description, tour_price = tour_price\
                start_date = start_date, end_date = end_date, ratings = ratings)

    database.session.add(u)
    database.session.commit()

   

    

 





