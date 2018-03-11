import os

from timeswitch.auth.model import create_db as auth_db_init
from timeswitch.switch.model import create_db as time_db_init
from timeswitch.switch.model import SwitchModel


def create_db(db_file):
    if os.path.exists(db_file):
        os.remove(db_file)
        auth_db_init()
        time_db_init()

def setup_model(app):
    create_db(app.config['DB_FILE'])
    return SwitchModel(app.config['DB_FILE'])