from flask import render_template
from . import app


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


@app.route("/login")
def login():
    return render_template("login.html", title="Login")

