from project.database import db
from sqlalchemy.sql import func
from marshmallow import Schema, fields, post_load, ValidationError


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
        self.lastname= lastname
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '{0} {1}: {2}'.format(self.firstname, self.lastname, self.email)

class UserSchema(Schema):
    id = fields.Int()
    firstname = fields.Str(
        required=True,
        error_messages={'required': 'A first name is a required'}
    )
    lastname = fields.Str(
        required=True,
        error_messages={'required': 'A last name is a required'}
    )
    username = fields.Str(
        required=True,
        error_messages={'required': 'A username is a required'}
    )
    email = fields.Email(
        required=True,
        error_messages={'required': 'A email address is a required'}
    )
    password = fields.Str(
        required=True,
        error_messages={'required': 'A password is a required'}
    )
    time_created = fields.DateTime()
    time_updated = fields.DateTime()

    @post_load
    def make_user(self, data):
        return User(**data)
