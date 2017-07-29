from flask import Flask, jsonify
from project.database import db
from project.user import User, UserSchema
from flask_restful import Resource, Api
from mixer.backend.flask import mixer

import os

app = Flask(__name__)
api = Api(app)
# app.secret_key = 'Test123'
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

api.add_resource(listUsers, '/Users', '/Users/')

class Users(Resource):
    def get(self, user_name):
        user = db.session.query(User).filter_by(username=user_name).first()
        schema = UserSchema()
        userJSON = schema.dump(user)
        return  userJSON

    def put(self, userObj):
        schema = UserSchema()
        user = schema.load(userObj)
        db.session.add(user.data)
        db.session.commit()
        return jsonify({'status': 'success'})

api.add_resource(Users, '/Users/<string:user_name>')

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