from flask import current_app as app

@app.route('/admin')
def admin_home():
    return "<h1>This is Admin Page</h1>"