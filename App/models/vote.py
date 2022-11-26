from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"), nullable=False)
    type = db.Column(db.String, nullable=False)
    # reviews = db.relationship(
    #     "Review", backref="user", lazy=True, cascade="all, delete-orphan"
    # )

    def __init__(self, staff_id, review_id, type):
        self.staff_id = staff_id
        self.review_id = review_id
        self.type = type