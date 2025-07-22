from .database import db
from .models import User, Role, Transaction
from flask import current_app as app, jsonify, request, render_template
from flask_security import auth_required, roles_required, current_user, roles_accepted, login_user
from werkzeug.security import check_password_hash, generate_password_hash

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

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

@app.route('/api/login', methods=['POST'])
def user_login():
    body = request.get_json()
    email = body.get('email')
    password = body.get('password')

    if not email:
        return jsonify({
            "message": "Email is required!"
        }), 400
    
    user = app.security.datastore.find_user(email=email)
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            print(current_user)
            return jsonify({
                    "id": user.id,
                    "username": user.username,
                    "auth-token": user.get_auth_token(),
                }), 200
            
        else:
            return jsonify({
                "message": "Invalid password!"
            }), 400
    else:
        return jsonify({
            "message": "User not found!"
        }), 404

@app.route('/api/register', methods=['POST'])
def create_user():
    credentials = request.get_json()
    if not app.security.datastore.find_user(email = credentials['email']):
        app.security.datastore.create_user(email = credentials['email'], username = credentials['username'], password = generate_password_hash(credentials['password']), roles = ['user'])
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

@app.route('/api/delivery/<int:trans_id>', method=['POST'])
@auth_required('token')
@roles_required('admin')
def delivery(trans_id):
    body = request.get_json()
    trans = Transaction.query.get(trans_id)
    trans.delivery_status = body['status']
    db.session.commit()
    return jsonify({
        "message": "Delivery status updated successfully",
    }), 200

@app.route('/api/review/<int:trans_id>', methods=['POST'])
@auth_required('token')
@roles_required('admin')
def review(trans_id):
    body = request.get_json()
    trans = Transaction.query.get(trans_id)
    trans.delivery = body['delivery']
    trans.amount = body['amount']
    trans.internal_status = 'pending'
    db.session.commit()
    return jsonify({
        "message": "Transaction reviewed successfully",
    }), 200