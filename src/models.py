import random
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

# Creating User Database model


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    point = db.Column(db.Integer, default=0)
    current_q = db.Column(db.Integer, default=1)
    current_custom_q = db.Column(db.Integer, default=1)
    current_qset = db.Column(db.Integer, default=lambda: random.randint(1, 8))
    done_qset = db.Column(db.String(50), default="")
    _password = db.Column(db.String(128), nullable=False)

    # secure password system using hash
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    # verify password by hash
    def verify_password(self, password):
        return check_password_hash(self._password, password)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # All relationships with other tables
    history = db.relationship('History', backref='user', lazy=True)
    custom_quiz = db.relationship('Custom_Quiz', backref='user', lazy=True)
    custom_quiz_history = db.relationship('Custom_Quiz_History', backref='user', lazy=True)

    # return user object
    def __repr__(self):
        return f'<User {self.username}>'


# Database model for System Questions
# Remember that the question set 101 is reserved for custom questions even though they has separate database but this set is reserved
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    qset = db.Column(db.Integer, nullable=False)
    qno = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(500), nullable=False)
    opt1 = db.Column(db.String(100), nullable=False)
    opt2 = db.Column(db.String(100), nullable=False)
    opt3 = db.Column(db.String(100), nullable=False)
    opt4 = db.Column(db.String(100), nullable=False)
    # ans should be like opt1, opt2, opt3, opt4
    ans = db.Column(db.String(10), nullable=False)
    pts = db.Column(db.Integer, nullable=False)
    history = db.relationship('History', backref='question', lazy=True)

    def __repr__(self):
        return f"<Question {self.qset} - {self.qno}>"


# Log of user's system given Question answers
class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    # Assuming user_ans is a string (option value like 'opt1', 'opt2', etc.)
    user_ans = db.Column(db.String(10), nullable=False)
    points = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<History User: {self.user_id}, Question: {self.question_id}, Answer: {self.user_ans}>"


# Database model for user created questions
class Custom_Quiz(db.Model):
    __tablename__ = 'custom_quiz'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False, unique=True)
    opt1 = db.Column(db.String(100), nullable=False)
    opt2 = db.Column(db.String(100), nullable=False)
    opt3 = db.Column(db.String(100), nullable=False)
    opt4 = db.Column(db.String(100), nullable=False)
    ans = db.Column(db.String(10), nullable=False)
    pts = db.Column(db.Integer, nullable=False)
    upvote = db.Column(db.Integer, default=0)
    downvote = db.Column(db.Integer, default=0)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    custom_quiz_history = db.relationship('Custom_Quiz_History', backref='custom_quiz', lazy=True)

    def __repr__(self):
        return f"<Custom_Quiz {self.id}>"


# Log of user's answered question from another onther user created question
class Custom_Quiz_History(db.Model):
    __tablename__ = 'custom_quiz_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('custom_quiz.id'))
    # Assuming user_ans is a string (option value like 'opt1', 'opt2', etc.)
    user_ans = db.Column(db.String(10), nullable=False)
    point = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Custom_Quiz_History User: {self.user_id}, Question: {self.question_id}, Answer: {self.user_ans}>"
