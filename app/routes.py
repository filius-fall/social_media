from flask import render_template, flash, redirect
from flask.helpers import url_for
from flask_login.utils import current_user, login_user
from werkzeug.security import check_password_hash
from . import app
from .forms import LoginForm
from .models import User


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="HOME")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/explore")
def explore():
    return render_template("explore.html", title="explore")


@app.route("/friends")
def friends():
    return render_template("friends.html", title="Friends")


@app.route("/register")
def register():
    return render_template("register.html", title="Registration")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for user {}".format(form.username.data))
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):

            flash("Username or Password is incorrect")
            return redirect(url_for("login"))
        login_user(user, remember=remember_me.data)
        return redirect("/home")
    return render_template("login.html", title="Login", form=form)

