from app import database
from app.models import User, Tour, UserFeedback
import math, random
from datetime import date
praise = ['Good', 'Amazing', 'Fantastic', 'Fabulous']
experience = ['Adventure', 'Tour', 'Experience']

# 100*10 permutations
for n in range(10+1):
    # Get list of user IDs
    users = User.get_all_users()
    upper_bound = len(users)
    for user in users:
        # Create feedback
        while True:
            rand = random.randint(1, upper_bound) 
            if rand != user.id:
                break
                
        _praise = praise[random.randrange(len(praise))] + ' ' + experience[random.randrange(len(experience))]
        ratings = round(random.uniform(1, 5),1)

        u = UserFeedback(user_id = rand, by_user_id = user.id, user_rating = ratings, user_feedback = _praise)
        database.session.add(u)
        database.session.commit()

