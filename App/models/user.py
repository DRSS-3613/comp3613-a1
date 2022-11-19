from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class User(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    access = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
"""
    def is_admin(self):
        return self.access == ACCESS["admin"]

    def allowed(self, access_level):
        return self.access >= access_level
"""

    def to_json(self):
        return {"id": self.id, "username": self.username}

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
