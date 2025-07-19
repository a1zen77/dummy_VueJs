from .database import db
from .models import User, Role, Transaction
from flask import current_app as app, jsonify, request
from flask_security import auth_required, roles_required, current_user, roles_accepted, hash_password

@app.route('/', methods=['GET'])
def home():
    return "<h1>Home Page</h1>"

@app.route('/api/admin')
@auth_required('token')
@roles_required('admin')
def admin_home():
    return jsonify({
        "message" : "admin logged in successfully"
    })

@app.route('/api/home')
@auth_required('token')
@roles_required(['user', 'admin'])
@roles_accepted(['user', 'admin'])
def user_home(user_id):
    user = current_user()
    return jsonify({    
        "username": user.username,
        "email": user.email,
        "password": user.password,
    })

@app.route('/api/register', methods=['POST'])
def create_user():
    credentials = request.get_json()
    if not app.security.datastore.find_user(email = credentials['email']):
        app.security.datastore.create_user(email = credentials['email'], username = credentials['username'], password = hash_password(credentials['password']), roles = ['user'])
        db.session.commit() 
        return jsonify({
            "message": "User created successfully"
        }), 201
    
    return jsonify({
        "message": "User already exists"
    }), 400

@app.route('/api/pay/<int:trans_id>')
@auth_required('token')
@roles_required('user')
def payment(trans_id):
    trans = Transaction.query.get(trans_id)
    trans.internal_status = 'paid'
    db.session.commit()
    return jsonify({
        "message": "Payment successful!",
    })