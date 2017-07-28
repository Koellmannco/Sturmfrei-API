from flask import Flask, jsonify
from project.database import db
from project.user import User
from flask_restful import Resource, Api
from mixer.backend.flask import mixer

import os

app = Flask(__name__)
api = Api(app)
# app.secret_key = 'Test123'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db.init_app(app)


@app.route('/')
def index():
    return "Hello, World! This is the Sturmfrei API"

class listUsers(Resource):
    def get(self):
        userList = []
        for user in db.session.query(User.username).order_by(User.id):
            userList.append(user)
        return jsonify({'userList': userList})

api.add_resource(listUsers, '/getUsers')

class Users(Resource):
    def get(self, user_name):
        user = db.session.query(User.username).filter_by(username=user_name).first()
        return jsonify({'user': user})

api.add_resource(Users, '/getUsers/<string:user_name>')

if __name__ == '__main__':
    app.run(debug=True)

# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     User1 = User(firstname='Austin', lastname='Brogan', username='arbrog',email='arbrog14@gmail.com', password='password123')
#     db.session.add(User1)
#     db.session.commit()
#     mixer.init_app(app)
#     users = mixer.cycle(10).blend(User)