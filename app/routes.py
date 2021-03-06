from operator import or_
from flask import render_template, flash, redirect, request
from flask.helpers import url_for
from flask.signals import request_tearing_down
from flask_login.utils import current_user, login_user
from werkzeug.security import check_password_hash
from wtforms.validators import url
from . import app, db
from .forms import LoginForm, RegistrationForm,EditProfileForm,EmptyForm,PostForm
from .models import User,Post
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/home",methods=['GET','Post'])
@login_required
def home():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(content=form.post.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('You have succesfully added some Bullshit on Internet')
        return redirect(url_for('home'))
    posts = current_user.followed_posts().all()
    return render_template("home.html", title="HOME", posts=posts,form=form)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/explore")
def explore():
    posts=Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("home.html", title="explore",posts=posts)


@app.route("/profile/<username>")
@login_required
def profile(username):
    form=EmptyForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = [{"author": user, "body": "Test 01"}, {"author": user, "body": "Test 02"}]
    return render_template("profile.html", user=user, posts=posts,form=form)


@app.route("/friends")
@login_required
def friends():
    return render_template("friends.html", title="Friends")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if current_user.is_authenticated:
#         redirect(url_for("home"))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash("Congrats! You have been registered")
#         return redirect(url_for("login"))
#     return render_template("register.html", title="Registration", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


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
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("home")
        return redirect(next_page)
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))



@app.route('/edit_profile',methods=["GET","POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Changes have been added')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form)


# @app.route('/follow/<username>')
# @login_required
# def follow(username):
#     form=EmptyForm()
#     if form.validate_on_submit():
#         user=User.query.filter_by(username=username).first()
#         if user is none:
#             flash('User {} not found'.format(username))
#             return redirect(url_for('home'))
#         if user==current_user:
#             flash('You cant follow yourself')
#             return redirect(url_for('profile',username=username))
#         current_user.follow(user)
#         db.session.commit()
#         flash('YOu are now following {}'.format(username))
#         return redirect(url_for('profile',username=username))
#     else:
#         return redirect(url_for('home'))



# @app.route('/unfollow/<usernmae>')
# @login_required
# def unfollow(username):
#     form=EmptyForm()
#     if form.validate_on_submit():
#         user=User.query.filter_by(username=username).first()
#         if user is None:
#             flash('User Not found')
#             return redirect(url_for('home'))
#         if user==current_user:
#             flash('You cannot unfollow yourself')
#             return redirect(url_for('profile'),username=username)
#         current_user.unfollow(user)
#         db.session.commit()
#         flash('You have now succesfully unfollowed {}'.format(username))
#         return redirect(url_for('profile',username=username))
#     else:
#         return redirect(url_for('home'))



@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('home'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('profile', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('profile', username=username))
    else:
        return redirect(url_for('home'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('home'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('profile', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('profile', username=username))
    else:
        return redirect(url_for('home'))