from flask import render_template, flash, redirect
from . import app
from .forms import LoginForm


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
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            "Login requested for user{}, remember_me={}".format(
                form.username.data, form.remember_me.data
            )
        )
        return redirect("/home")
    return render_template("login.html", title="Login", form=form)

