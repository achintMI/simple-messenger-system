from datetime import datetime

import jwt
from flask import Blueprint, request, jsonify
from sqlalchemy import func

from src.extensions import db
from src.models import Users, Messages, LastRead, TOKEN_SECRET_KEY

messaging_bp = Blueprint('messaging', __name__)


def verify_token(f):
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Missing token. Please provide a valid token.'}), 401

        try:
            payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = Users.query.get(user_id)
            if not user:
                return jsonify({'message': 'Invalid token. User not found.'}), 401

            # Add the user object to the function arguments so we can access it in the API endpoint
            kwargs['user'] = user
            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired. Please log in again.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token. Please provide a valid token.'}), 401

    decorated_function.__name__ = f.__name__
    return decorated_function


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


@messaging_bp.route('/get/users', methods=['GET'])
def get_users():
    users = Users.query.with_entities(Users.username).all()
    users_list = [u.username for u in users]
    return jsonify({'status': 'success', 'data': users_list}), 200


@messaging_bp.route('/send/text/user', methods=['POST'])
@verify_token
def send_text(user):
    data = request.get_json()
    receiver_username = data.get('tousername', None)
    message_text = data.get('text', None)

    if not receiver_username or not message_text:
        return jsonify({'status': 'failure', 'message': 'receiver and message content are required'}), 400

    receiver = Users.query.filter_by(username=receiver_username).first()
    if not receiver:
        return jsonify({'status': 'failure', 'message': 'receiver not found'}), 404

    new_message = Messages(sender_id=user.id, receiver_id=receiver.id, message=message_text)
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'status': 'success'}), 201


@messaging_bp.route('/get/unread', methods=['GET'])
@verify_token
def get_unread(user):
    last_read = LastRead.query.filter_by(user_id=user.id).first()
    if last_read:
        last_read_timestamp = last_read.last_read_at
        last_read.last_read_at = datetime.utcnow()
    else:
        last_read_timestamp = datetime.min
        last_read = LastRead(user_id=user.id)

    db.session.add(last_read)
    db.session.commit()

    unread_messages_data = (
        db.session.query(Messages.sender_id, Messages.message, Users.username)
        .join(Users, Messages.sender_id == Users.id)
        .filter(Messages.sent_at > last_read_timestamp)
        .all()
    )

    unread_messages_list = []
    total_unread_count = 0
    for sender_id, message_text, sender_username in unread_messages_data:
        total_unread_count += 1
        for msg_data in unread_messages_list:
            if msg_data['username'] == sender_username:
                msg_data['texts'].append(message_text)
                break
        else:
            unread_messages_list.append({'username': sender_username, 'texts': [message_text]})

    if total_unread_count == 0:
        message = "No new messages"
    else:
        message = f'You have {total_unread_count} new message' + ('s' if total_unread_count > 1 else '')

    response_data = {
        'status': 'success',
        'message': message,
        'data': unread_messages_list
    }

    return jsonify(response_data), 200


@messaging_bp.route('/get/history', methods=['GET'])
@verify_token
def get_history(user):
    from_username = request.args.get('fromusername')
    if not from_username:
        return jsonify({'status': 'failure', 'message': 'Please provide the fromusername parameter.'}), 400

    from_user = Users.query.filter_by(username=from_username).first()
    if not from_user:
        return jsonify({'status': 'failure', 'message': 'fromusername not found.'}), 404

    chat_history = (
        Messages.query.filter(
            (Messages.sender_id == user.id) & (Messages.receiver_id == from_user.id) |
            (Messages.sender_id == from_user.id) & (Messages.receiver_id == user.id)
        )
        .order_by(Messages.sent_at)
        .all()
    )

    chat_history_list = [message.message for message in chat_history]

    response_data = {
        'status': 'success',
        'texts': chat_history_list
    }

    return jsonify(response_data), 200