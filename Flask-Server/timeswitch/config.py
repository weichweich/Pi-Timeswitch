KEY_DB_FILE = "DB_FILE"

class Config(object):
    DEBUG = False
    TESTING = False
    DB_FILE = 'sqlite://:memory:'
    SECRET_KEY = 'NOT_SO_SECRET'
