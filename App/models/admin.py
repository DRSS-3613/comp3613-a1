from .user import User
from .student import Student
from App.database import db

class Admin (User):
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.access = "admin"
    

    def toJSON(self):
        return{
            'id': self.id,
            'username': self.username,
            'access': 'admin'
        }
    
    #only admin can create Student objects
    def create_student(name,school_id,faculty, programme):
        try:
            new_student = Student(name=name, school_id=school_id, programme=programme, faculty=faculty)
            db.session.add(new_student)
            db.session.commit()
            return new_student
        except Exception as e:
            print('Error creating student', e)
            db.session.rollback()
            return None
