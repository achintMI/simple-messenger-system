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
