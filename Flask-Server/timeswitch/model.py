import os
import logging

from timeswitch.auth.model import create_db as auth_db_init
from timeswitch.switch.model import create_db as time_db_init
from timeswitch.switch.model import SwitchModel
from timeswitch.config import KEY_DB_FILE

_LOG = logging.getLogger(__name__)

def create_db(db_file):
    auth_db_init()
    time_db_init()

def setup_model(app, clean_db=False):
    if clean_db:
        os.remove(app.config[KEY_DB_FILE])

    if not os.path.isfile(app.config[KEY_DB_FILE]):
        with app.app_context():
            _LOG.info("create db (%s)", app.config[KEY_DB_FILE])
            create_db(app.config[KEY_DB_FILE])

    return SwitchModel(app.config[KEY_DB_FILE])