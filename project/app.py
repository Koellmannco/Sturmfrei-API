from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL")
db = SQLAlchemy(app)
db.create_all()

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
    username = db.Column('username', db.Unicode)
    email = db.Column('email', db.Unicode)
    password = db.Column('password', db.Unicode)
    register_date = db.Column('register_date',db.TIMESTAMP, default=datetime.now())

    def __repr__(self):
        return '<User %r>' % (self.name)
