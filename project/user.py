from project.database import db
from sqlalchemy.sql import func
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

    # def __init__(self, name, username, email, password):
    #     self.name = name
    #     self.username = username
    #     self.email = email
    #     self.password = password

    def __repr__(self):
        return '{0} {1}: {2}'.format(self.name, self.username, self.email)
