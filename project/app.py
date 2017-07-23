from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#import os
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://sturmfrei_api_DB:2Fm82iFHgmFCR8DBJsFe@sturmfrei-api-database01.cnxqjx6tjodx.us-east-1.rds.amazonaws.com/sturmfrei_api"
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Unicode(30))
    username = db.Column(db.Unicode(25), nullable=False)
    email = db.Column(db.Unicode(40), nullable=False)
    password = db.Column(db.Unicode(32), nullable=False)
    register_date = db.Column(db.TIMESTAMP, default=datetime.now())

db.drop_all()
db.create_all()
User1 = User(name='Austin',username='arbrog',email='arbrog@gmail.com', password='password123')
db.session.add(User1)
db.session.commit()

@app.route('/')
def index():
    return "Hello, World! This is the Sturmfrei API"

if __name__ == '__main__':
    app.run(debug=True)

    def __repr__(self):
        return '<User %r>' % (self.name)
