# -*- coding: utf-8 -*-

import logging
import json
from datetime import datetime

from flask import request, current_app, g
from flask_restful import Resource, abort
import bcrypt
import jwt
from marshmallow import ValidationError

import auth
from auth.schema import UserSchema

class NullHandler(logging.Handler):
	def emit(self, record):
		pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)

class LoginResource(Resource):
	method_decorators = []

	def post(self):
		json_data = request.get_json(force=True)
		
		if 'name' not in json_data:
			LOGGER.info('Access denied: No username given.')
			return "No username found.", 400
		elif 'password' not in json_data:
			LOGGER.info('Access denied: No password given.')
			return "No password found.", 400

		try:
			user_name = json_data['name']
			password = json_data['password']

			if not auth.check_password(auth.get_user(user_name), password):
				LOGGER.info('Access denied: wrong password.')
				return "Invalide password or username.", 400
		except LookupError:
			LOGGER.info('Access denied: User not found. {}'.format(user_name))
			return "Invalide password or username.", 400
		except Exception as e:
			LOGGER.warn('Access denied: unknown error: {}'.format(e))
			return "Unknowen error.", 500

		LOGGER.info('User {0} logged in.'.format(json_data['name']))
		
		token = auth.create_token(auth.get_user(json_data['name']))
		body_json = { 'token': token }

		return json.dumps(body_json), 200

class UsersResource(Resource):
	method_decorators = [auth.dec_auth]

	def __init__(self):
		self.schema = UserSchema(many=True)
		self.method_decorators = [auth.dec_auth]

	def get(self):
		'''Get all user names and privileges'''
		resources = auth.get_users()
		result = self.schema.dump(resources)
		return result.data, 200

class UserResource(Resource):

	def __init__(self):
		self.schema = UserSchema(many=False)
		self.method_decorators = [auth.dec_auth]

	def get(self, user_name):
		'''Get all user names and privileges'''
		resources = auth.get_user(user_name)
		result = self.schema.dump(resources)
		return result.data, 200

	def post(self, user_name):
		'''Create a new user'''
		request_json = request.get_json(force=True)
		try:
			self.schema.validate(request_json)
		except ValidationError as err:
			LOGGER.warn("ValidationError POST \n\t"\
				+ str(err.messages) + "\n" + str(request_json))
			return err.messages, 400
		except IncorrectTypeError as err:
			LOGGER.warn("IncorrectTypeError POST \n\t"\
			 + str(err.messages) + "\n" + str(request_json))
			return err.messages, 400

		result = self.schema.load(request_json)

		auth.add_user(result.data)

		updated_result = self.schema.dump(result.data)
		return updated_result.data, 200

	def delete(self, user_name):
		'''delete an existing user'''
		auth.remove_user(user_name)
		return 204

	def patch(self, user_name):
		'''update password and/or privilege of an user'''
		request_json = request.get_json(force=True)
		try:
			self.schema.validate(request_json)
		except ValidationError as err:
			LOGGER.warn("ValidationError POST \n\t"\
				+ str(err.messages) + "\n" + str(request_json))
			return err.messages, 400
		except IncorrectTypeError as err:
			LOGGER.warn("IncorrectTypeError POST \n\t"\
			 + str(err.messages) + "\n" + str(request_json))
			return err.messages, 400

		resource = self.schema.load(request_json)
		auth.update_user(resource)
		result = self.schema.dump(resource)
		return result.data, 200
