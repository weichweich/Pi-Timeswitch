# -*- coding: utf-8 -*-

import bcrypt
import logging
import sqlite3 as sql
from flask import request, current_app, g
from datetime import datetime, timedelta

from auth.dao import User

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)

# Privileges

PRIVILEGE_ADMIN = 1
PRIVILEGE_USER  = 0

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
            pwd_salted_hashed = bcrypt.hashpw(password_clear.encode('utf-8'), bcrypt.gensalt())
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
                WHERE name=?''', (user_name,))
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

def update_user(user, password_clear):
    with sql.connect(current_app.config['SQL_FILE']) as connection:
        cur = connection.cursor()
        pwd_salted_hashed = bcrypt.hashpw(password_clear.encode('utf-8'), bcrypt.gensalt())
        val = (user.name, user.privilege, user.last_loggin, pwd_salted_hashed)
        cur.execute('''REPLACE INTO
                User(name, privilege, last_loggin, password)
                VALUES (?, ?, ?, ?)''', vals)
