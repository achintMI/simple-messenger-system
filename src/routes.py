import bcrypt
from flask import Blueprint, request, jsonify
from src.extensions import db
from src.models import Users

messaging_bp = Blueprint('messaging', __name__)


@messaging_bp.route('/create/user', methods=["post"])
def create_user():
    request_data = request.get_json()
    username = request_data.get('username', None)
    passcode = request_data.get('passcode', None)
    if not username or not passcode:
        return jsonify({'status': "failure", 'message': 'username and passcode are required'}), 400

    if Users.query.filter_by(username=username).first():
        return jsonify({'status': "failure", 'message': 'user already exists'}), 400

    new_user = Users(username=username, password=passcode)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'status': 'success'})


@messaging_bp.route("/login", methods=["post"])
def login():
    request_data = request.get_json()
    username = request_data.get('username', None)
    passcode = request_data.get('passcode', None)

    if not username or not passcode:
        return jsonify({'status': 'failure', 'message': 'username and passcode are required'}), 400

    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({'status': 'failure', 'message': 'invalid credentials, user mot found'}), 401

    if not user.verify_password(passcode):
        return jsonify({'status': 'failure', 'message': 'invalid credentials, incorrect passcode'}), 401

    return jsonify({'status': 'success', 'token': user.generate_token()}), 200
