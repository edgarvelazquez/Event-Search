from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


@login.user_loader
def lode_user(user_id):
    return User.query.get(user_id)


# assistant table between two users
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email= db.Column(db.String(128),index=True, unique=True)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_pw(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_pw(self, pw):
        return check_password_hash(self.password_hash, pw)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def un_follow(self,user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self,user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(followers,(followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id =self.id)
        return followed.union(own).order_by(Post.timestamp.desc())



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post {self.body}>'


class Event(db.Model):
    id = db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(256), index=True)
    category = db.Column(db.String(256), index=True)
    address = db.Column(db.String(256), index=True)
    img_url = db.Column(db.String(256), index=True)
    event_url = db.Column(db.String(256), index=True)
    date = db.Column(db.String(256), index=True)
    description = db.Column(db.String(256), index=True)



class Favourite(db.Model):
    user_id = db.Column(db.String(256), primary_key=True)
    event_id = db.Column(db.String(256), primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
