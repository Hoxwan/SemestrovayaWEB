from flask_httpauth import HTTPTokenAuth
from app.models import User
from app import db

token_auth = HTTPTokenAuth(scheme='Bearer')

@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None

@token_auth.error_handler
def token_auth_error(status):
    return {'message': 'Authentication required'}, status