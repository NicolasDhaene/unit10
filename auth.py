from flask import g

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

import models

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Token')
auth = MultiAuth(token_auth, basic_auth)


@basic_auth.verify_password
def verify_password(username_or_token, password):
    user = models.User.verify_auth_token(username_or_token)
    if not user:
        user = models.User.get(
            (models.User.email == username_or_token)|
            (models.User.username == username_or_token)
        )
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@token_auth.verify_token
def verify_token(token):
    user = models.User.verify_auth_token(token)
    if user is not None:
        g.user = user
        return True
    return False