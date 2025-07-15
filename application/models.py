from flask_sqlalchemy import SQLAlchemy
from .database import db
from flask_security import UserMixin, RoleMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fs_uniquifier = db.Column(db.String, unique = True, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    roles = db.relationship('Role', backref = 'bearer', secondary='user_roles')
    trans = db.relationship('Transaction', backref='bearer')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String(255))

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    delivery = db.Column(db.String, nullable=False, default='to be updated')
    source = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    internal_status = db.Column(db.String, nullable=False, default='requested')
    delivary_status = db.Column(db.String, nullable=False, default='in process')
    description = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, default=1000)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))