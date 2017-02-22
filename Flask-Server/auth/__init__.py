# -*- coding: utf-8 -*-

from functools import wraps
import sqlite3 as sql
import logging
from datetime import datetime, timedelta
import os

from flask import request, current_app, g
from flask_restful import abort
import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError, DecodeError, \
						   ExpiredSignatureError, InvalidAlgorithmError, \
						   MissingRequiredClaimError

from auth.dao import User

class NullHandler(logging.Handler):
	def emit(self, record):
		pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)



# Privileges

PRIVILEGE_ADMIN = 1
PRIVILEGE_USER  = 0

JWT_EXPERATIONTIME = {
	"days":1,
	"seconds":0,
	"microseconds":0,
	"milliseconds":0,
	"minutes":0,
	"hours":0,
	"weeks":0
}


def create_db():
	'''Creates User table.'''
	with sql.connect(current_app.config['SQL_FILE']) as connection:
		cur = connection.cursor()
		cur.execute('''CREATE TABLE User(
			id INTEGER PRIMARY KEY,
			name TEXT,
			password TEXT,
			last_loggin INTEGER,
			privilege INTEGER,
			email TEXT,
			CONSTRAINT unique_name UNIQUE (name))''')

	add_user(User('admin', PRIVILEGE_ADMIN, user_id=-1, last_loggin=datetime.utcnow()), \
				  'admin')

def add_user(user, password_clear=None):
	with sql.connect(current_app.config['SQL_FILE']) as connection:
		cur = connection.cursor()

		pwd_salted_hashed = ''
		if password_clear is not None: 
			pwd_salted_hashed = bcrypt.hashpw(password_clear, bcrypt.gensalt())
		else:
			pwd_salted_hashed = user.pwd_salty_hash

		vals = (user.name, pwd_salted_hashed, user.last_loggin, \
				user.privilege, user.email)
		cur.execute('''INSERT INTO
			User(name, password, last_loggin, privilege, email)
			VALUES (?, ?, ?, ?, ?)''', vals)
		user.id = cur.lastrowid


def get_user(user_name):
	with sql.connect(current_app.config['SQL_FILE']) as connection:
		cur = connection.cursor()

		cur.execute('''SELECT * FROM User
				WHERE name = ?''', (user_name,))
		row = cur.fetchone()
		if row is None:
			raise LookupError('User not found!')

		return User(user_id=row[0], name=row[1], pwd_salty_hash=row[2],\
					privilege=row[4], last_loggin=row[3], email=row[5])

def get_users():
	with sql.connect(current_app.config['SQL_FILE']) as connection:
		cur = connection.cursor()

		cur.execute('''SELECT * FROM User''')
		rows = cur.fetchall()
		users = []
		for row in rows:
			users.append(User(user_id=row[0], name=row[1], pwd_salty_hash=row[2],\
					privilege=row[4], last_loggin=row[3], email=row[5]))

		return users

def remove_user(user_name):
	with sql.connect(current_app.config['SQL_FILE']) as connection:
		cur = connection.cursor()
		cur.execute('''DELETE FROM User
		            WHERE name=?''', (user_name,))

def update_user(user, password_clear=None):
	with sql.connect(current_app.config['SQL_FILE']) as connection:
		cur = connection.cursor()
		pwd_salted_hashed = bcrypt.hashpw(password_clear, bcrypt.gensalt())
		val = (user.name, user.privilege, user.last_loggin, pwd_salted_hashed)
		cur.execute('''REPLACE INTO
				User(name, privilege, last_loggin, password)
				VALUES (?, ?, ?, ?)''', vals)

def create_token(user):
	secret = current_app.config['SECRET_KEY']
	jwt_token = jwt.encode({
			'user': user.name,
			'id': user.id,
			'iat': datetime.utcnow(),
			'exp': datetime.utcnow() + timedelta(**JWT_EXPERATIONTIME)
		}, secret, algorithm='HS256')
	return str(jwt_token)

def check_password(user_name, plain_text_password):
    # Check hashed password. Useing bcrypt, 
    # the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def dec_auth(func):
	@wraps(func)
	def func_wrapper(*args, **kwargs):
		secret_key = current_app.config['SECRET_KEY']
		try:
			token_data = jwt.decode(request.headers['auth'], \
				                    secret_key, algorithm='HS256')
			LOGGER.warn("Token check not implemented")

			if 'user' in token_data:
				LOGGER.info("ACCESS GRANTED: User {0} {1} {2}"
							.format(token_data['user'], \
									request.method, request.url))
				user = get_user(token_data['user'])
				if user is None:
					msg="User is not known!"
					abort(401, description=msg)
					return
				g.auth_user = user
			else:
				msg="Missing data in token!"
				abort(401, description=msg)
				return

		except InvalidTokenError:
			msg="The supplied token was not valide!"
			abort(401, description=msg)
			return
		except DecodeError:
			msg="The token was not singed corretly!"
			abort(401, description=msg)
			return
		except ExpiredSignatureError:
			msg="The token expired!"
			abort(401, description=msg)
			return
		except InvalidAlgorithmError:
			msg="The used algorithem is not suppoerted by the server!"
			abort(401, description=msg)
			return
		except MissingRequiredClaimError:
			msg="The token is missing a claim!"
			abort(401, description=msg)
			return
		except KeyError:
			msg="The token is not provided!"
			abort(401, description=msg)
			return
		except Exception as e:
			msg="Unknown token error!"
			LOGGER.warn(str(e))
			abort(401, description=msg)
			return
		return func(*args, **kwargs)

	return func_wrapper
