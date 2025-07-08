from flask import Flask
from application.database import db
from application.config import LocalDevelopmentConfig
from application.models import User, Role, UserRoles
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import hash_password

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)

    app.app_context().push()

    return app

app = create_app()

with app.app_context():
    db.create_all()

    app.security.datastore.find_or_create_role(name='admin', description='Super User')
    app.security.datastore.find_or_create_role(name='user', description='Regular User')
    db.session.commit()

    if not app.security.datastore.find_user(email = 'user@admin.com'):
        app.security.datastore.create_user(email = 'user@admin.com', username = 'admin01', password = hash_password('12345'))

if __name__ == "__main__":
    app.run()


