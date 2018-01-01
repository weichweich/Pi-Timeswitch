import json
import logging
import os
from datetime import datetime, timedelta
from functools import wraps

import bcrypt
import jwt
from flask import current_app, g, request
from flask_restful import abort
from jwt.exceptions import (DecodeError, ExpiredSignatureError,
                            InvalidAlgorithmError, InvalidTokenError,
                            MissingRequiredClaimError)

from timeswitch.auth.dao import User
from timeswitch.auth.model import get_user_with_name


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


logging.getLogger(__name__).addHandler(NullHandler())
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


def __make_auth_error(code, detail):
    return {
        'status': '401',
        'code': code,
        'title': 'Authentication Error',
        'detail': detail,
        'source': {
            'pointer': request.url
        }
    }


def dec_auth(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        secret_key = current_app.config['SECRET_KEY']
        errors = []

        try:
            token_data = jwt.decode(request.headers['auth'],
                                    secret_key, algorithm='HS256')

            if 'user' in token_data:
                LOGGER.info("ACCESS GRANTED: User {0} {1} {2}"
                            .format(token_data['user'],
                                    request.method, request.url))
                user = get_user_with_name(token_data['user'])
                if user is None:
                    msg = "User is not known!"
                    errors.append(__make_auth_error(401, msg))
                else:
                    g.auth_user = user
            else:
                msg = "Missing data in token!"
                errors.append(__make_auth_error(401, msg))

        except DecodeError:
            msg = "The token was not singed corretly!"
            errors.append(__make_auth_error(401, msg))
        except ExpiredSignatureError:
            msg = "The token expired!"
            errors.append(__make_auth_error(401, msg))
        except InvalidAlgorithmError:
            msg = "The used algorithem is not suppoerted by the server!"
            errors.append(__make_auth_error(401, msg))
        except MissingRequiredClaimError:
            msg = "The token is missing a claim!"
            errors.append(__make_auth_error(401, msg))
        except InvalidTokenError:
            msg = "The supplied token was not valide!"
            errors.append(__make_auth_error(401, msg))
        except KeyError:
            msg = "The token is not provided!"
            errors.append(__make_auth_error(401, msg))

        if errors:
            return func(*args, **kwargs)
        else:
            return {'errors': errors}, 401

    return func_wrapper
