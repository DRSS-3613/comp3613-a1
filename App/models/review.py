from App.database import db

import datetime
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    timestamp = db.Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    sentiment = db.Column(db.String, db.ForeignKey("sentiment"),nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    votes = db.Column(MutableDict.as_mutable(JSON), nullable=False)

    def __init__(self, staff_id, student_id, sentiment, text):
        self.staff_id = staff_id
        self.student_id = student_id
        self.timestamp = datetime.datetime.utcnow
        self.sentiment = sentiment
        self.text = text
        self.votes = {"num_upvotes": 0, "num_downvotes": 0}

    def vote(self, user_id, vote):
        self.votes.update({user_id: vote})
        self.votes.update(
            {"num_upvotes": len([vote for vote in self.votes.values() if vote == "up"])}
        )
        self.votes.update(
            {
                "num_downvotes": len(
                    [vote for vote in self.votes.values() if vote == "down"]
                )
            }
        )

    def get_num_upvotes(self):
        return self.votes["num_upvotes"]

    def get_num_downvotes(self):
        return self.votes["num_downvotes"]

    def get_all_votes(self):
        return self.votes

    def to_json(self):
        return {
            "id": self.id,
            "staff_id": self.staff_id,
            "student_id": self.student_id,
            "text": self.text,
            "sentiment":self.sentiment,
            "num_upvotes": self.get_num_upvotes(),
            "num_downvotes": self.get_num_downvotes(),
        }
