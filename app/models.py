from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from hashlib import md5


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    about_me=db.Column(db.String(200))
    posts = db.relationship("Post", backref="author", lazy=True)

    # followed = db.relationship(
    #     'User',secondary=followers,
    #     primaryjoin=(followers.c.follower_id==id),
    #     secondaryjoin=(followers.c.followed_id==id)
    #     backref=db.backref('followers',lazy='dynamic'),lazy='dynamic'
    # )

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password_hash):
        self.password = generate_password_hash(password_hash)

    def check_password(self, password_hash):
        return check_password_hash(self.password, password_hash)

    def avatar(self,size):
        digest=md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id==user.id).count()>0

    def followed_posts(self):
        followed = Post.query.join(followers.c.followed_id==user_id).filter(followers.c.follower_id)
        own = Post.query.filter_by(user_id==self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.content}', '{self.timestamp}')"




