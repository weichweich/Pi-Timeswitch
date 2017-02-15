# -*- coding: utf-8 -*-

import logging
import time

from flask import request
from flask_restful import Resource

from marshmallow import ValidationError, post_load, validates_schema
from marshmallow_jsonapi import Schema, fields
from marshmallow_jsonapi.exceptions import IncorrectTypeError


from auth.dao import User

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
	id = fields.Str(dump_only=True)

	name = fields.String(required=True)
	email = fields.String(required=False)
	last_loggin = fields.String(required=False)
	privilege = fields.Integer(required=False)

	@post_load
	def make_user(self, data):
		return User(**data)

	def handle_error(self, exc, data):
		raise ValidationError('An error occurred with input: {0} \n {1}'.format(data, str(exc)))

	class Meta:
		type_ = 'user'
		# inflect = dasherize
