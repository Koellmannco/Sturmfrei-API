from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL")
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column( db.Integer, primary_key=True, nullable=False)
    name = db.Column( db.Unicode(30))
    username = db.Column( db.Unicode(25), nullable=False, unique=True)
    email = db.Column(db.Unicode(40), nullable=False, unique=True)
    password = db.Column( db.Unicode(32), nullable=False)
    register_date = db.Column( db.TIMESTAMP, default=datetime.now())

@app.route('/')
def index():
    return "Hello, World! This is the Sturmfrei API"

@app.route('/getUsers', methods=['GET'])
def getUsers():
    userList=[]
    for user in db.session.query(User.username).order_by(User.id):
        userList.append(user)
    return jsonify({'userList': userList})
    
@app.route('/getUsers/<int:user_id', methods=['GET'])
def getUsers(int user_id):
    userData=[db.session.query(User).filter(User.id=user_id)]
    return jsonify({'userData': userData})
if __name__ == '__main__':
    app.run(debug=True)

    def __repr__(self):
        return '<User %r>' % (self.name)

#db.drop_all()
#db.create_all()
#User1 = User(name='Austin1',username='arbrog1',email='arbrog1@gmail.com', password='password123')
#db.session.add(User1)
#db.session.commit()
