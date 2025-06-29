from flask import request, jsonify
import bcrypt
import jwt
import datetime
from functools import wraps
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv('MONGO_URI')
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['market_metrics']
users_collection = db['users']

SECRET_KEY = os.getenv('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'success': False, 'error': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = users_collection.find_one({'email': data['email']})
            if not current_user:
                raise Exception('User not found')
        except Exception as e:
            return jsonify({'success': False, 'error': 'Token is invalid or expired!'}), 401
        return f(*args, **kwargs)
    return decorated

def init_auth_routes(app):
    @app.route('/signup', methods=['POST'])
    def signup():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            if not email or not password:
                return jsonify({'success': False, 'error': 'Email and password required'}), 400
            if users_collection.find_one({'email': email}):
                return jsonify({'success': False, 'error': 'Email already exists'}), 400
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            users_collection.insert_one({'email': email, 'password': hashed_pw})
            # Generate JWT token on signup
            token = jwt.encode({
                'email': email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, SECRET_KEY, algorithm='HS256')
            return jsonify({'success': True, 'message': 'User registered successfully', 'token': token})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    @app.route('/signin', methods=['POST'])
    def signin():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            if not email or not password:
                return jsonify({'success': False, 'error': 'Email and password required'}), 400
            user = users_collection.find_one({'email': email})
            if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
                return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
            # Generate JWT token on successful signin
            token = jwt.encode({
                'email': email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, SECRET_KEY, algorithm='HS256')
            return jsonify({'success': True, 'message': 'Sign-in successful', 'token': token})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    @app.route('/protected', methods=['GET'])
    @token_required
    def protected():
        return jsonify({'success': True, 'message': 'This is a protected route'})

    return app 