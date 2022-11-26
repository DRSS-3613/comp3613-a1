from App.models import User
from App.database import db


# Creates a new user given their email, password and access level
def create_user(email, password, firstName, lastName, access=1):
    new_user = User(email=email, password=password, firstName=firstName, lastName=lastName, access=access)
    db.session.add(new_user)
    db.session.commit()
    return new_user


# Gets a user by their email
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


# Gets a user by their id
def get_user(id):
    return User.query.get(id)


# Gets all users that have a certain access level
def get_users_by_access(access):
    return User.query.filter_by(access=access).all()


# Gets all users in the database
def get_all_users():
    return User.query.all()


# Gets all users and returns them as a JSON object
def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    return [user.to_json() for user in users]


# Updates a user's email given their id and email
def update_user(id, email):
    user = get_user(id)
    if user:
        user.email = email
        db.session.add(user)
        return db.session.commit()
    return None


# Deletes a user given their id
def delete_user(id):
    user = get_user(id)
    if user:
        db.session.delete(user)
        return db.session.commit()
    return None
