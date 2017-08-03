from flask import Flask, jsonify, request, json, abort
from project.database import db
from project.user import User, UserSchema
from flask_restful import Resource, Api
from project.database_error_handler import database_error_handler
from project.validation_errors import handle_validation_errors
#from mixer.backend.flask import mixer

import os

app = Flask(__name__)
api = Api(app)
app.secret_key = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def index():
    return "Hello, World! This is the Sturmfrei API landing page"


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
    method_decorators = [database_error_handler]

    def get(self):
        user = User.query(User).filter_by(username="arbrog").first()
        schema = UserSchema()
        userJSON = schema.dump(user)
        return jsonify({'result': userJSON})

    def put(self):
        schema = UserSchema()
        user, error = schema.loads(request.data)
        handle_validation_errors(error)
        db.session.add(user)
        db.session.commit()
        #print(error)

    def post(self):
        data = json.loads(request.data)
        errors = UserSchema().validate(data, partial=True )
        handle_validation_errors(errors)
        if 'id' in data:
            user = User.query.filter_by(id=data['id']).first()
            if user is not None:
                for key, value in data.items():
                    if key == 'firstname':
                        user.firstname = value
                    if key == 'lastname':
                        user.lastname = value
                    if key == 'email':
                        user.email = value
                    if key == 'username':
                        user.username = value
                db.session.commit()
            else:
                abort(404, "user does not exist")
        else:
            abort(404, "missing user id")


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
