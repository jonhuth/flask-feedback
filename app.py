from flask import (Flask, request, redirect,
                   render_template, flash, session)
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, AddFeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "super secret"

connect_db(app)
db.create_all()


@app.route('/')
def redirect_register():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()

    if form.validate_on_submit():
        user_attrs = {
            'username': form.username.data,
            'password': form.password.data,
            'email': form.email.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data
        }

        # new_user = User(**user_attrs)
        new_user = User.register(**user_attrs)
        db.session.add(new_user)
        db.session.commit()

        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session["username"] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Bad name/password"]
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop("username")
    return redirect('/')


@app.route('/users/<username>')
def show_secret(username):
    if "username" in session:
        user = User.query.get(username)
        return render_template('user.html', user=user)
    return redirect('/login')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def show_feedback_form(username):
    # user = User.query.get(username)
    if username == session['username']:
        form = AddFeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_feedback = Feedback(title=title, 
                                    content=content, username=username)
            db.session.add(new_feedback)
            db.session.commit()
            flash("Feedback added!")
            return redirect(f"/users/{username}")
        else:
            flash("Please login")
            return render_template('add-feedback-form.html', form=form)
    # else if "username" not in session:
        # and is a different user, log into their PF page
    else:
        return redirect("/login")


@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    # pretty much need this whenever you have a user
    if "username" not in session:
        flash("Please login")
        return redirect("/login")
    if feedback.username == session['username']:
        form = AddFeedbackForm(title=feedback.title, content=feedback.content)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            flash("Feedback edited!")
            return redirect(f"/users/{feedback.username}")
        else:
            return render_template('edit-feedback-form.html', form=form)
    else:
        return redirect(f"/user/{feedback.username}")


@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted!")
        return redirect(f"/users/{feedback.username}")
    else:
        return redirect("/login")


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    user = User.query.get(username)
    if username == session['username']:
        db.session.delete(user)
        db.session.commit()

        # remove the user from the session
        session.pop("username")

        flash("User deleted!")

        return redirect(f"/login")
    else:
        return redirect("/login")