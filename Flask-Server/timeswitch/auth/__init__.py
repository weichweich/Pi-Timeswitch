# -*- coding: utf-8 -*-

import logging
from functools import wraps
from flask import current_app, g, request

from timeswitch.auth.model import get_user_with_name
from timeswitch.auth.helper import create_token, check_password, get_hashed_password
import jwt
from jwt.exceptions import (DecodeError, ExpiredSignatureError,
                            InvalidAlgorithmError, InvalidTokenError,
                            MissingRequiredClaimError)

LOGGER = logging.getLogger(__name__)

def _make_auth_error(code, detail):
    error = {
        'status': '401',
        'code': code,
        'title': 'Authentication Error',
        'detail': detail,
        'source': {
            'pointer': request.url
        	}
    	}
    return error

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
                    errors.append(_make_auth_error(401, msg))
                else:
                    g.auth_user = user
            else:
                msg = "Missing data in token!"
                errors.append(_make_auth_error(401, msg))

        except DecodeError:
            msg = "The token was not singed corretly!"
            errors.append(_make_auth_error(401, msg))
        except ExpiredSignatureError:
            msg = "The token expired!"
            errors.append(_make_auth_error(401, msg))
        except InvalidAlgorithmError:
            msg = "The used algorithem is not suppoerted by the server!"
            errors.append(_make_auth_error(401, msg))
        except MissingRequiredClaimError:
            msg = "The token is missing a claim!"
            errors.append(_make_auth_error(401, msg))
        except InvalidTokenError:
            msg = "The supplied token was not valide!"
            errors.append(_make_auth_error(401, msg))
        except KeyError:
            msg = "The token is not provided!"
            errors.append(_make_auth_error(401, msg))

        if len(errors) == 0:
            return func(*args, **kwargs)
        else:
            return {'errors': errors}, 401

    return func_wrapper
