from flask import redirect, Response
from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import HTTPException
from .extensions import auth

class AuthException(HTTPException):
    """
    HTTPException wrapper class to get authentication exceptions used with flask_basicauth
    """
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'} ))

class AuthModelView(ModelView):
    """
    ModelView wrapper class to use flask_basicauth authentication with flask_admin views
    """
    def is_accessible(self):
        if not auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(auth.challenge())