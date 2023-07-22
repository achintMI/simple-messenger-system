import jwt
from src.extensions import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    passcode = db.Column(db.String(128), nullable=False)
    token = db.relationship('Tokens', backref='users', lazy=True)

    def generate_token(self):
        expiration = datetime.utcnow() + timedelta(hours=1)
        payload = {'user_id': self.id, 'exp': expiration}
        token = jwt.encode(payload, 'some_secret_key', algorithm='HS256')
        return token

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, passcode):
        self.passcode = generate_password_hash(passcode)


class Tokens(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
