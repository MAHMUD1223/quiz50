from . import app, db
from .models import User, Question, History, Custom_Quiz, Custom_Quiz_History
from .forms import Login, Register, Edit, Create_Quiz
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, fresh_login_required, current_user

# Index route


@app.route("/")
def index():
    users = User.query.order_by(User.point.desc()).all()
    return render_template("index.html", users=users)

# Login route


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()  # Initializing form
    # Checking if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST" and form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        # Checking if username already exists
        if not user:
            flash("Invalid username!", "danger")
            return redirect(url_for("login"))
        # Verifying password
        if user.verify_password(password):
            login_user(user)  # Login user
            session.permanent = True  # Setting session time see `__init__.pya`
            flash("Login successful", category="success")
            # Redirecting to the page where user was before login
            if request.form.get("next"):
                return redirect(request.form.get("next"))
            return redirect(url_for("index"))
        else:
            flash("Invalid password!", category="danger")
            # Passing the page where user was before login as a parameter
            if request.form.get("next"):
                return redirect(url_for("login", next=request.form.get("next")))
    else:
        # Flashing errors
        for err in form.errors.values():
            flash(f"error {err}", category='danger')
    return render_template("auth/login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Register()  # Initializing form
    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("confirmation")
        # Checking if username already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please try another", "danger")
            return redirect(url_for("register"))
        # Creating user
        create_user = User(username=username, password=password)
        db.session.add(create_user)
        db.session.commit()
        flash("User created successfully", "success")
        return redirect(url_for("login"))
    else:
        # Flashing errors
        for err in form.errors.values():
            flash(f"error {err}", category='danger')
    return render_template("auth/register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()  # Logout user
    return redirect(url_for("login"))


@app.route("/edit-profile", methods=["GET", "POST"])
@fresh_login_required
def edit_profile():
    form = Edit()  # Initializing form
    if form.validate_on_submit():
        username = request.form.get("username")
        edit_user = User.query.filter_by(username=current_user.username).first()
        # Checking if username already exists
        if User.query.filter_by(username=username).first() and username != current_user.username:
            flash("Username already exists. Please try another", "danger")
            return redirect(url_for("edit_profile"))
        edit_user.username = username
        if request.form.get("confirmation"):
            edit_user.password = request.form.get("confirmation")
        db.session.commit()
        flash("Profile updated successfully", "success")
        return redirect(url_for("profile"))
    else:
        # Flashing errors
        for err in form.errors.values():
            flash(f"error {err}", category='danger')
    return render_template("profile/edit-profile.html", form=form)


@app.route("/profile")
@login_required
def profile():
    # Getting user System history
    history = db.session.query(History, Question).join(Question, History.question_id == Question.id).filter(
        History.user_id == current_user.id).order_by(History.id.desc()).all()
    # Getting user created quiz
    created_quiz = db.session.query(Custom_Quiz, User).join(
        Custom_Quiz, Custom_Quiz.created_by == User.id).filter(Custom_Quiz.created_by == current_user.id).all()
    # Getting user quiz history that was created by other users
    custom_history = db.session.query(Custom_Quiz_History, Custom_Quiz).join(Custom_Quiz, Custom_Quiz_History.question_id == Custom_Quiz.id).filter(
        Custom_Quiz_History.user_id == current_user.id).order_by(Custom_Quiz_History.id.desc()).all()
    elem = len(history)+1
    return render_template("profile/profile.html", history=history, elem=elem, created_quiz=created_quiz, custom_history=custom_history)


@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    # Fetching question from database
    question = Question.query.filter(
        Question.qset == current_user.current_qset, Question.qno == current_user.current_q).first_or_404()
    # Creating question dictionary to pass to template and verify answer
    ques = {
        "question": question.question,
        "opt1": question.opt1,
        "opt2": question.opt2,
        "opt3": question.opt3,
        "opt4": question.opt4
    }
    if request.method == "POST":
        answer = request.form.get("option")
        # Getting correct answer
        correct_ans = ques[question.ans]
        # Creating history
        history = History(user_id=current_user.id, question_id=question.id, user_ans=answer)
        # Verifying answer
        if answer == correct_ans:
            # Adding points
            current_user.point += question.pts
            history.points = question.pts
            flash("Correct answer!", "success")
        else:
            history.points = 0
            flash("Worng answer", "warning")
            flash("Correct answer was "+correct_ans, "info")
        # Updating user current question and question set
        if current_user.current_q == 25:
            current_user.current_q = 1
            current_user.done_qset += str(current_user.current_qset) + ","
            if current_user.current_qset == 8:
                current_user.current_qset = 1
            else:
                current_user.current_qset += 1
        else:
            current_user.current_q += 1
        db.session.add(history)
        db.session.commit()
        return redirect(url_for("quiz"))
    return render_template("quiz/quiz.html", question=ques)


@app.route("/quiz/create", methods=["GET", "POST"])
@login_required
def create_quiz():
    form = Create_Quiz()  # Initializing form
    if form.validate_on_submit():
        question = request.form.get("question")
        opt1 = request.form.get("opt1")
        opt2 = request.form.get("opt2")
        opt3 = request.form.get("opt3")
        opt4 = request.form.get("opt4")
        ans = request.form.get("ans")
        pts = request.form.get("pts")
        # Creating quiz
        create_quiz = Custom_Quiz(question=question, opt1=opt1, opt2=opt2,
                                  opt3=opt3, opt4=opt4, ans=ans, pts=pts, created_by=current_user.id)
        db.session.add(create_quiz)
        db.session.commit()
        flash("Quiz created successfully. Thank you for your contribution", "success")
        return redirect(f"{url_for('create_quiz')}#created-quiz")
    else:
        # Flashing errors
        for err in form.errors.values():
            flash(f"error {err}", category='danger')
    return render_template("quiz/quiz-create.html", form=form)


@app.route("/quiz/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_quiz(id):
    # Fetching quiz from database to edit
    quiz = Custom_Quiz.query.filter(
        Custom_Quiz.id == id, Custom_Quiz.created_by == current_user.id).first_or_404()
    if request.method == "POST":
        # Updating quiz
        quiz.opt1 = request.form.get("opt1")
        quiz.opt2 = request.form. get("opt2")
        quiz.opt3 = request.form.get("opt3")
        quiz.opt4 = request.form.get("opt4")
        quiz.ans = request.form.get("answer")
        db.session.commit()
        flash("Quiz updated successfully", "success")
        return redirect(f"{url_for('profile')}#created-quiz")
    return render_template("quiz/quiz-edit.html", quiz=quiz)


@app.route("/quiz/delete/<id>")
@login_required
def delete_quiz(id):
    # Deleting quiz
    quiz = Custom_Quiz.query.filter(
        Custom_Quiz.id == id, Custom_Quiz.created_by == current_user.id).first_or_404()
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz deleted successfully", "success")
    return redirect(url_for("profile"))


@app.route("/quiz/101", methods=["GET", "POST"])
@login_required
def quiz_101():
    # Fetching other user created quiz from database
    quiz = Custom_Quiz.query.filter(Custom_Quiz.id == current_user.current_custom_q).first()
    # Checking if quiz is available
    if quiz == None:
        flash("No more custom Quiz available now. Please try again later", "info")
        return redirect(url_for("profile"))
    # Checking if user is trying to access his own quiz
    if quiz.created_by == current_user.id:
        current_user.current_custom_q += 1
        db.session.commit()
        return redirect(url_for("quiz_101"))
    # Creating question dictionary to pass to template and verify answer
    question = {
        "question": quiz.question,
        "opt1": quiz.opt1,
        "opt2": quiz.opt2,
        "opt3": quiz.opt3,
        "opt4": quiz.opt4,
        'upvote': quiz.upvote,
        'downvote': quiz.downvote,
        "credit": User.query.filter_by(id=quiz.created_by).first().username
    }
    if request.method == "POST":
        vote = request.form.get("vote")
        # Checking if user voted
        if vote:
            if vote == "upvote":
                quiz.upvote += 1
            elif vote == "downvote":
                quiz.downvote += 1
        answer = request.form.get("option")
        # Getting correct answer
        correct_ans = question[quiz.ans]
        # Creating history in custom quiz history
        history = Custom_Quiz_History(user_id=current_user.id, question_id=quiz.id, user_ans=answer)
        # Verifying answer
        if answer == correct_ans:
            current_user.point += quiz.pts
            history.point = quiz.pts
            flash("Correct answer!", "success")
        else:
            history.point = 0
            flash("Worng answer", "warning")
            flash("Correct answer was "+correct_ans, "info")
        current_user.current_custom_q += 1
        db.session.add(history)
        db.session.commit()
        return redirect(url_for("quiz_101"))
    return render_template("quiz/quiz101.html", question=question)


@app.route("/about")
def about():
    # About page
    return render_template("about.html")


@app.route("/contact")
def contact():
    # Contact page
    return render_template("contract.html")
