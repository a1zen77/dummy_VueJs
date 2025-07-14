from flask import current_app as app, jsonify
from flask_security import auth_required, roles_required, current_user

@app.route('/admin')
@auth_required('token')
@roles_required('admin')
def admin_home():
    return jsonify({
        "message" : "admin logged in successfully"
    })

@app.route('/user')
def user_home(user_id):
    user = current_user()
    return jsonify({    
        "username": user.username,
        "email": user.email,
        "password": user.password,
    })