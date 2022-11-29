from App.database import db
import math 

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    faculty = db.Column(db.String(100), nullable=False)
    programme = db.Column(db.String(100), nullable=False)
    reviews = db.relationship("Review", backref="student", lazy=True, cascade="all, delete-orphan")

    def __init__(self, firstName, lastName, faculty, programme):
        self.firstName = firstName
        self.lastName = lastName
        self.faculty = faculty
        self.programme = programme

# (total ups if positive + downs if negative) / total votes
    def get_karma(self):
        total_positivity = 0
        total_votes=0
        for review in self.reviews:
            if review.sentiment=="positive":
                total_positivity += review.get_num_upvotes()
            if review.sentiment=="negative":
                total_positivity+=review.get_num_downvotes()
            total_votes += review.get_num_votes()
        if not total_votes:
            return total_votes
        return math.ceil((total_positivity/total_votes) * 100)


    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "faculty": self.faculty,
            "programme": self.programme,
            "karma": self.get_karma(),
        }
