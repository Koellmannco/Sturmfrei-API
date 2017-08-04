from project.database import db
from sqlalchemy.sql import func
from flask import g
from marshmallow import Schema, fields, post_load
from itsdangerous import Serializer, SignatureExpired, BadSignature, TimedJSONWebSignatureSerializer
from flask_httpauth import HTTPBasicAuth

import os

auth = HTTPBasicAuth()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
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
            print("get user by id")
            return User.query.filter_by(id=user_id).first()
        elif username:
            print("get user by username")
            return User.query.filter_by(username=username).first()
        print("user not found")
        return None

    def __repr__(self):
        return '{0} {1}: {2}'.format(self.firstname, self.lastname, self.email)

    def generate_auth_token(self, expiration=600):
        s = TimedJSONWebSignatureSerializer(
            os.environ.get("SECRET_KEY"),
            expires_in=expiration
        )
        return s.dumps({'id': self.id})

    def verify_password(self, password):
        return self.password == password

    @staticmethod
    def verify_auth_token(token):
        s = TimedJSONWebSignatureSerializer(
            os.environ.get("SECRET_KEY"),
            expires_in=600
        )
        try:
            data = s.loads(token)
        except SignatureExpired:
            print("sign expired")
            return None  # valid token, but expired
        except BadSignature:
            print("sign invalid")
            return None  # invalid token
        print(data['id'])
        user = User.get(user_id=data['id'])
        return user


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    print("verify based on token")
    print(username_or_token)
    user = User.verify_auth_token(username_or_token)
    if not user:
        print("verify based on credentials")
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
