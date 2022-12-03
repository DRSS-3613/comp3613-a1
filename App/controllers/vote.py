from App.models import Vote
from App.database import db

# gets all votes for a review
def get_all_votes(review_id):
    return Vote.query.filter_by(review_id=review_id)

# gets all votes for a review
def get_all_votes_json(review_id):
    votes = get_all_votes(review_id)
    return [vote.to_json() for vote in votes]