from app import database
from app.models import User, Tour, TourParticipant
import math, random
from datetime import date
praise = ['Good', 'Amazing', 'Fantastic', 'Fabulous']
experience = ['Adventure', 'Tour', 'Experience']

# 100*10 permutations
for n in range(10+1):
    # Get list of tour IDs
    tours = Tour.get_tours().all()
    user = User.get_all_users()
    upper_bound = len(tours)
    for tour in tours:
        # Create feedback
        while True:
            rand = random.randint(1, upper_bound) 
            if rand != tour.user_id:
                break
                
        _praise = praise[random.randrange(len(praise))] + ' ' + experience[random.randrange(len(experience))]
        ratings = round(random.uniform(1, 5))

        u = TourParticipant(tour_id = tour.id, user_id = rand, tour_user_rating = ratings, tour_user_feedback = _praise)
        database.session.add(u)
        database.session.commit()

