# -*- coding: utf-8 -*-

class User:
	
	def __init__(self, name, privilege, \
				 last_loggin=None, email=None, pwd_salty_hash=None, id=-1):
		self.id = id
		self.name = name
		self.pwd_salty_hash = pwd_salty_hash
		self.last_loggin = last_loggin
		self.privilege = privilege
		self.email = email
