from datetime import datetime
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login


@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))


class Permissions:
    READ = 0x01
    COMMENT = 0x02
    WRITE = 0x04
    MODERATE = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=1)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    projects = db.relationship('Project', backref='author', lazy='dynamic')
    events = db.relationship('Event', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions == permissions)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=600, token_type='reset_password'):
        return jwt.encode(
            {token_type: self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_token(token, token_type='reset_password'):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])[token_type]
        except Exception as e:
            current_app.logger.error('Error {}'.format(e))
            return
        return db.session.query(User).get(id)

    def is_admin(self):
        return self.email in current_app.config['ADMINS']

    @staticmethod
    def insert_roles():
        roles = {
            'User': Permissions.READ | Permissions.WRITE | Permissions.COMMENT,
            'Moderator': Permissions.READ | Permissions.WRITE | Permissions.COMMENT | Permissions.MODERATE,
            'Administrator': 0xff
        }
        for r in roles:
            role = db.session.query(Role).filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r]
            db.session.add(role)
            db.session.commit()


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    name = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user_home = db.Column(db.String(512))
    project_home = db.Column(db.String(512))
    app_home = db.Column(db.String(512))
    archive = db.Column(db.String(512))
    packages = db.Column(db.String(512))


class FeedBack(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    email = db.Column(db.String(512))
    content = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
