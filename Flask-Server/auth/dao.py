# -*- coding: utf-8 -*-

class User:
	def __init__(self, name, privilege, \
				 last_loggin=None, email=None, pwd_salty_hash=None, \
				 password_clear=None, newPassword=None, user_id=-1):
		self.id = user_id
		self.name = name

		#TODO: remove password chaos! Where to store and how to pass new passwords. Cleartext vs. hash...
		self.pwd_salty_hash = pwd_salty_hash
		self.password_clear = password_clear
		self.newPassword = newPassword
		self.last_loggin = last_loggin
		self.privilege = privilege
		self.email = email
