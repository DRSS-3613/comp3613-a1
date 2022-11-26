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
    # votes = db.Column(MutableDict.as_mutable(JSON), nullable=False)
    votes = db.relationship("Vote", backref="Review", lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, staff_id, student_id, sentiment, text):
        self.staff_id = staff_id
        self.student_id = student_id
        self.timestamp = datetime.datetime.utcnow
        self.sentiment = sentiment
        self.text = text
    
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
        
    def get_upvotes(self):
        return self.query.filter(self.votes.type == "up") 
    
    def get_downvotes(self):
        return self.query.filter(self.votes.type == "down") 
    
    def get_num_upvotes(self):
        count = 0
        for v in self.get_upvotes(): count+=1
        return count
    
    def get_num_downvotes(self):
        count = 0
        for v in self.get_downvotes(): count+=1
        return count
    
    def get_num_votes(self):
        return self.get_num_upvotes() + self.get_num_downvotes()