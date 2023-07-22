import bcrypt
from flask import Blueprint, request, jsonify
from src.extensions import db
from src.models import Users, Tokens

messaging_bp = Blueprint('messaging', __name__)


@messaging_bp.route('/create/user', methods=["post"])
def create_user():
    request_data = request.get_json()
    username = request_data.get('username', None)
    passcode = request_data.get('passcode', None)
    if not username or not passcode:
        return jsonify({'status': "failure", 'message': 'username or passcode is required'}), 400

    if Users.query.filter_by(username=username).first():
        return jsonify({'status': "failure", 'message': 'user already exists'}), 400

    new_user = Users(username=username, passcode=passcode)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'status': 'success'})