from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):  # Create table Users
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='Author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):  # Create hash password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):  # Check hash password
        return check_password_hash(self.password_hash, password)


class Post(db.Model):  # Create table Posts
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Item(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_author = db.Column(db.String(120))
    name_item = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __repr__(self):
        return '<Name author: {}, Body: {}>'.format(self.name_author, self.name_item)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
