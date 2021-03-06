from project.database import db
from sqlalchemy.sql import func
from flask import g
from marshmallow import Schema, fields, post_load
from itsdangerous import SignatureExpired, BadSignature, TimedJSONWebSignatureSerializer
from flask_httpauth import HTTPBasicAuth
from project.security import pwd_context

import os

auth = HTTPBasicAuth()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, firstname, lastname, username, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def get(user_id=None, username=None):
        if user_id:
            return User.query.filter_by(id=user_id).first()
        elif username:
            return User.query.filter_by(username=username).first()
        return None

    def set_password(self, new_pass):
        new_hash = pwd_context.hash(new_pass)
        self.password = new_hash

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = TimedJSONWebSignatureSerializer(
            os.environ.get("SECRET_KEY"),
            expires_in=expiration
        )
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = TimedJSONWebSignatureSerializer(
            os.environ.get("SECRET_KEY"),
        )
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.get(user_id=data['id'])
        return user

    def __repr__(self):
        return '{0} {1}: {2}'.format(self.firstname, self.lastname, self.email)


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.get(username=username_or_token)  # based on credentials
        if not user or not user.verify_password(password):
            return False
        g.user = user
    return True


class UserSchema(Schema):
    id = fields.Int()
    firstname = fields.Str(
        required=True
    )
    lastname = fields.Str(
        required=True
    )
    username = fields.Str(
        required=True
    )
    email = fields.Email(
        required=True
    )
    password = fields.Str(
        load_only=True,
        required=True
    )
    time_created = fields.DateTime(dump_only=True)
    time_updated = fields.DateTime(dump_only=True)

    # class Meta:
    #     fields = ("id", "firstname", "lastname", "username", "email", "password", "time_created", "time_updated")
    #     ordered = True

    @post_load
    def make_user(self, data):
        return User(**data)
