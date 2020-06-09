from flask import (Flask, request, redirect,
                   render_template, flash, session)
from models import db, connect_db, User
from forms import RegisterUserForm, LoginUserForm

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
