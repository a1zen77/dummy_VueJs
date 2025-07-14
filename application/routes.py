from flask import current_app as app, jsonify
from flask_security import auth_required, roles_required, current_user, roles_accepted

@app.route('/admin')
@auth_required('token')
@roles_required('admin')
def admin_home():
    return jsonify({
        "message" : "admin logged in successfully"
    })

@app.route('/user')
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