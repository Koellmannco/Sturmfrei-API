from flask import Flask, jsonify
from project.database import db
from project.user import User
from flask_restful import Resource, Api

import os

app = Flask(__name__)
api = Api(app)
# app.secret_key = 'Test123'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db.init_app(app)


@app.route('/')
def index():
    return "Hello, World! This is the Sturmfrei API"

class getUsers(Resource):
    def get(self):
        userList = []
        for user in db.session.query(User.username).order_by(User.id):
            userList.append(user)
        return jsonify({'userList': userList})

api.add_resource(getUsers, '/getUsers')

class getUser(Resource):
    def get(self, user_id):
        user = db.session.query(User.username).first()
        return jsonify({'user': user})

api.add_resource(getUser, '/getUsers/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)

#with app.app_context():
   # db.drop_all()
  #  db.create_all()
  #  User1 = User(name='Austin1',username='arbrog1',email='arbrog1@gmail.com', password='password123')
   # db.session.add(User1)
   # db.session.commit()
