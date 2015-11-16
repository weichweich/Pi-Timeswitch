#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from flask_restful import Api

from time_switch.switch_manager import SwitchManager
from time_switch.model import create_db, PiSwitchModel
from resources import PinsResource, SequencesResource, PinResource,\
                      SequenceResource, PinSchema

import argparse
import logging

# ######################################
# # parsing args
# ######################################

PARSER = argparse.ArgumentParser(description='Timeswitch for the\
 GPIOs of an Raspberry Pi with a webinterface.')
PARSER.add_argument('--file', dest='schedule_file', metavar='file',
                    type=str,
                    help='A JSON-file containing the schedule.',
                    required=True)

PARSER.add_argument('--debug', dest='debug', default=False,
                    const=True, nargs="?",
                    help='A JSON-file containing the schedule.')

PARSER.add_argument('--create', dest='create', default=False, const=True, nargs="?",
                    help='Creates a new database. DELETES ALL DATA!!')

ARGS = PARSER.parse_args()

# ######################################
# # Logging:
# ######################################

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-20s \
                    %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='piSwitch.log',
                    filemode='a')
# define a Handler which writes INFO messages or higher to the sys.stderr
CONSOLE = logging.StreamHandler()

if ARGS.debug:
    CONSOLE.setLevel(logging.DEBUG)
else:
    CONSOLE.setLevel(logging.INFO)

# set a format which is simpler for console use
FORMATTER = logging.Formatter('%(levelname)-8s:%(name)-8s:%(message)s')
# tell the handler to use this format
CONSOLE.setFormatter(FORMATTER)
# add the handler to the root logger
logging.getLogger('').addHandler(CONSOLE)

LOGGER = logging.getLogger("MAIN")

# ######################################
# # Setup Flask, flask_restful, switch_manager
# ######################################

SCHEDULE_FILE = ARGS.schedule_file

if ARGS.create:
    create_db(SCHEDULE_FILE)

SWITCH_MODEL = PiSwitchModel(SCHEDULE_FILE)
SWITCH_MANAGER = SwitchManager(SWITCH_MODEL)

PIN_SCHEMA = PinSchema(many=True)

# make static folder the main '/' folder... Part 1/2
APP = Flask(__name__, static_url_path='')
API = Api(APP)

# ######################################
# # routes:
# ######################################

# make static folder the main '/' folder... Part 2/2
@APP.route('/')
def root():
    return APP.send_static_file('index.html')

@APP.route('/shutdown')
def shutdown():
    SWITCH_MANAGER.stop()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

# ######################################
# # flask_restful:
# ######################################

resource_kwargs = {'switch_manager':SWITCH_MANAGER}

API.add_resource(PinsResource, '/api/pins',
                 resource_class_kwargs=resource_kwargs)

API.add_resource(PinResource, '/api/pins/<int:pin_id>',
                 resource_class_kwargs=resource_kwargs)

API.add_resource(SequencesResource, '/api/pins/<int:pin_id>/sequences', '/api/sequences',
                 resource_class_kwargs=resource_kwargs)

API.add_resource(SequenceResource, '/api/sequence/<int:sequence_id>',
                 resource_class_kwargs=resource_kwargs)

if __name__ == '__main__':

    SWITCH_MANAGER.start()
    try:
        APP.run(debug=ARGS.debug)
    finally:
        SWITCH_MANAGER.stop()
        LOGGER.info("############# END OF LOG #############\n")
