from .database import db
from .models import User, Role
from flask import current_app as app, jsonify
from flask_security import auth_required, roles_required, current_user, roles_accepted

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