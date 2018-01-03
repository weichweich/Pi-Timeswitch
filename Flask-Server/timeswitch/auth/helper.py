import json
import logging
import os
from datetime import datetime, timedelta

import bcrypt
import jwt
from flask import current_app, g, request
from flask_restful import abort
from jwt.exceptions import (DecodeError, ExpiredSignatureError,
                            InvalidAlgorithmError, InvalidTokenError,
                            MissingRequiredClaimError)

from timeswitch.auth.dao import User

LOGGER = logging.getLogger(__name__)


__JWT_EXPERATIONTIME = {
    "days": 1,
    "seconds": 0,
    "microseconds": 0,
    "milliseconds": 0,
    "minutes": 0,
    "hours": 0,
    "weeks": 0
}


def create_token(user):
    secret = current_app.config['SECRET_KEY']
    jwt_token = jwt.encode({
        'user': user.name,
        'id': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(**__JWT_EXPERATIONTIME)
    }, secret, algorithm='HS256')
    return jwt_token.decode('utf-8')


def check_password(user, plain_text_password):
    # Check hashed password. Useing bcrypt,
    # the salt is saved into the hash itself
    hashed_password = user.pwd_salty_hash
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())
