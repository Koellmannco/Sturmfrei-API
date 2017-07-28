from project.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30))
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    register_date = db.Column(db.TIMESTAMP, default=datetime.now())

    # def __init__(self, name, username, email, password):
    #     self.name = name
    #     self.username = username
    #     self.email = email
    #     self.password = password

    def __repr__(self):
        return '{0} {1}: {2}'.format(self.name, self.username, self.email)
