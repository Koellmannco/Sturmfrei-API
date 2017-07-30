from flask import Flask, jsonify, request
from project.database import db
from project.user import User, UserSchema
from flask_restful import Resource, Api
from mixer.backend.flask import mixer
import logging

import os

app = Flask(__name__)
api = Api(app)
app.secret_key = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def index():
    return "Hello, World! This is the Sturmfrei API"

class listUsers(Resource):
    def get(self):
        userList = []
        for user in db.session.query(User).order_by(User.id):
            userList.append(user)
        schema = UserSchema(many=True)
        result = schema.dump(userList)
        return jsonify({'result': result})

api.add_resource(listUsers, '/Users')

class Users(Resource):
    def get(self):
        user = db.session.query(User).filter_by(username="arbrog").first()
        schema = UserSchema()
        userJSON = schema.dump(user)
        return jsonify({'result': userJSON})

    def put(self):
        schema = UserSchema()
        logging.debug("test")
        logging.info(request.get_data())
        user = schema.load(request.get_data())
        print(user)
        #db.session.add(user)
        #db.session.commit()
        return jsonify({'response': 'user'})

api.add_resource(Users, '/Users/')

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