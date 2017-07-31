from sqlalchemy.exc import DBAPIError
from functools import wraps
from flask import abort

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
        if True:  # not app.config.get('TESTING', False):
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