from flask import Flask, jsonify, request, abort
from project.database import db
from project.user import User, UserSchema
from flask_restful import Resource, Api
from sqlalchemy.exc import DBAPIError
from functools import wraps
from mixer.backend.flask import mixer

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
    #method_decorators = [database_error_handler]
    def get(self):
        user = db.session.query(User).filter_by(username="arbrog").first()
        schema = UserSchema()
        userJSON = schema.dump(user)
        return jsonify({'result': userJSON})

    def put(self):
        schema = UserSchema()
        user,error = schema.loads(request.data)
        handle_validation_errors(error)
        db.session.add(user)
        db.session.commit()
        print(error)

api.add_resource(Users, '/Users/')

if __name__ == '__main__':
    app.run(debug=True)


def handle_validation_errors(errors):
    if len(errors):
        errorString = ''
        for k in errors:
            errorString += k + ' '
            for error in errors[k]:
                errorString += error + ', '
            errorString += '\n'
        abort(409, errorString)

def database_error_handler(f):
    """
    Use like so:

    class Users(Resource):
      method_decorators = [database_error_handler]
      def get(...):
        ...
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        if True: #not app.config.get('TESTING', False):
            try:
                ret = f(*args, **kwargs)
            except DBAPIError as e:
                diag = e.__cause__.diag
                msg = diag.message_detail or diag.message_primary or diag.message_hint or str(e.__class__.__name__)
                abort(409, msg)

            return ret
        else:
            return f(*args, **kwargs)

    return decorator

# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     User1 = User(firstname='Austin', lastname='Brogan', username='arbrog',email='arbrog14@gmail.com', password='password123')
#     db.session.add(User1)
#     db.session.commit()
#     mixer.init_app(app)
#     users = mixer.cycle(10).blend(User)
