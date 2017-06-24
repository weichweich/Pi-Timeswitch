# -*- coding: utf-8 -*-

import bcrypt
import logging
import sqlite3 as sql
from flask import request, current_app, g
from datetime import datetime, timedelta

from auth.dao import User
import auth

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())
LOGGER = logging.getLogger(__name__)

class Unauthorized(Exception):
    """Exception raised when there is an unauthorized attemt to access the database."""
    pass

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

def get_user(user_id):
    with sql.connect(current_app.config['SQL_FILE']) as connection:
        cur = connection.cursor()

        cur.execute('''SELECT * FROM User
                WHERE id=?''', (user_id,))
        row = cur.fetchone()
        if row is None:
            raise LookupError('User not found! (id == {})'.format(user_id))

        return User(user_id=row[0], name=row[1], pwd_salty_hash=row[2],\
                    privilege=row[4], last_loggin=row[3], email=row[5])

def get_user_with_name(username):
    with sql.connect(current_app.config['SQL_FILE']) as connection:
        cur = connection.cursor()

        cur.execute('''SELECT * FROM User
                WHERE name=?''', (username,))
        row = cur.fetchone()
        if row is None:
            raise LookupError('User not found! (name == {})'.format(username))

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

def remove_user(user_id):
    with sql.connect(current_app.config['SQL_FILE']) as connection:
        cur = connection.cursor()
        cur.execute('''DELETE FROM User
                    WHERE id=?''', (user_id,))

def update_user(user):
    old_user = get_user(user.id)
    if not auth.check_password(old_user, user.password_clear):
        raise Unauthorized("Users password does not match!")

    password_hash = old_user.pwd_salty_hash
    if not user.newPassword is None:
        password_hash = auth.get_hashed_password(user.newPassword.encode('utf-8'))

    with sql.connect(current_app.config['SQL_FILE']) as connection:
        cur = connection.cursor()
        val = (user.name, user.privilege, password_hash, user.id)
        cur.execute('''UPDATE User
                SET name=?, privilege=?, password=?
                WHERE id=?''', val)
    connection.close()

