from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL")
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    name = db.Column("name", db.Unicode(30))
    username = db.Column("username", db.Unicode(25), nullable=False)
    email = db.Column("email", db.Unicode(40), nullable=False)
    password = db.Column("password", db.Unicode(32), nullable=False)
    register_date = db.Column("register_date", db.TIMESTAMP, default=datetime.now())

@app.route('/')
def index():
    return "Hello, World! This is the Sturmfrei API"

if __name__ == '__main__':
    app.run(debug=True)

    def __repr__(self):
        return '<User %r>' % (self.name)

#db.drop_all()
#db.create_all()
#User1 = User(name='Austin4',username='arbrog4',email='arbrog4@gmail.com', password='password123')
#db.session.add(User1)
#db.session.commit()
