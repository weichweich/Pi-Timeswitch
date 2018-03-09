import logging

from marshmallow import ValidationError, post_load
from marshmallow_jsonapi import Schema, fields

from timeswitch.auth.dao import User


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)

class AppError(Exception):
    pass

def dasherize(text):
    return text.replace('_', '-')

class UserSchema(Schema):
    id = fields.String(dump_only=True, required=True)

    name = fields.String(required=True)
    password = fields.String(load_only=True, required=False, attribute="password_clear")
    new_password = fields.String(load_only=True, required=False)
    email = fields.Email(required=False)
    last_loggin = fields.String(required=False)
    privilege = fields.String(required=False)

    @post_load
    def make_user(self, data):
        return User(**data)

    def handle_error(self, exc, data):
        raise ValidationError('An error occurred with input: {0} \n {1}'.format(data, str(exc)))

    class Meta:
        type_ = 'users'
        # inflect = dasherize
