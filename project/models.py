from project import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User_Course(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    the_user = db.relationship("User", backref="x")
    the_course = db.relationship("Course", backref="x")



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)



class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)