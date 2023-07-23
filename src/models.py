import jwt
from src.extensions import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

TOKEN_SECRET_KEY = "token_secret_key"


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    passcode = db.Column(db.String(128), nullable=False)
    tokens = db.relationship('Tokens', backref='user', lazy=True)
    last_reads = db.relationship('LastRead', backref='user', lazy=True)

    def generate_token(self):
        expiration = datetime.utcnow() + timedelta(hours=1)
        payload = {'user_id': self.id, 'exp': expiration}
        token = jwt.encode(payload, TOKEN_SECRET_KEY, algorithm='HS256')
        return token

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        return self.passcode

    @password.setter
    def password(self, passcode):
        self.passcode = generate_password_hash(passcode)

    def verify_password(self, passcode):
        return check_password_hash(self.passcode, passcode)


class Messages(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Message %r>' % self.id


class LastRead(db.Model):
    __tablename__ = "last_read"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    last_read_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Tokens(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)