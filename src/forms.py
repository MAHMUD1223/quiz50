from .models import Custom_Quiz, Question
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo, Optional, ValidationError
from wtforms import StringField, PasswordField, SubmitField, SelectField


# Form for user login
class Login(FlaskForm):
    username = StringField(label="username", validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


# Form for user registration
class Register(FlaskForm):
    username = StringField(label="username", validators=[
        Length(max=20), DataRequired()])
    password = PasswordField(label="password1", validators=[
        Length(min=8, max=20), DataRequired()])
    confirmation = PasswordField(label="password1", validators=[Length(
        min=8, max=20), EqualTo("password"), DataRequired()])
    submit = SubmitField(label="Submit")

# Form for user information edit


class Edit(FlaskForm):
    username = StringField(label="username", validators=[Length(max=20), Optional()])
    password = PasswordField(label="password1", validators=[Length(min=8, max=20), Optional()])
    confirmation = PasswordField(label="password1", validators=[
                                 Length(min=8, max=20), EqualTo("password"), Optional()])
    submit = SubmitField(label="Submit")

# Form for creating Quiz


class Create_Quiz(FlaskForm):
    question = StringField(label="question", validators=[DataRequired()])
    # Checking if another question already exists

    def validate_question(self, question):
        quiz0 = Question.query.filter_by(question=question.data).first()
        quiz = Custom_Quiz.query.filter_by(question=question.data).first()
        if quiz or quiz0:
            raise ValidationError("Question already exists")
    opt1 = StringField(label="option1", validators=[DataRequired()])
    opt2 = StringField(label="option2", validators=[DataRequired()])
    opt3 = StringField(label="option3", validators=[DataRequired()])
    opt4 = StringField(label="option4", validators=[DataRequired()])
    ans = SelectField(label="answer", choices=[("opt1", "Option 1"), ("opt2", "Option 2"), (
        "opt3", "Option 3"), ("opt4", "Option 4")], validators=[DataRequired()])
    pts = SelectField(label="points", choices=[
                      (3, "Easy"), (5, "Medium"), (10, "Hard")], validators=[DataRequired()])
    submit = SubmitField(label="Submit")
