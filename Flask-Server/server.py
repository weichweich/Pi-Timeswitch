# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_restful import Api

from time_switch.switch_manager import SwitchManager
from time_switch.model import create_db, PiSwitchModel
from schema import PinSchema, SequenceSchema
from resources import ManyRessource, SingleResource

import argparse
import logging

# ######################################
# # parsing commandline args
# ######################################

PARSER = argparse.ArgumentParser(description='Timeswitch for the\
 GPIOs of an Raspberry Pi with a webinterface.')
PARSER.add_argument('--file', dest='schedule_file', metavar='file',
                    type=str, default='gpio_time.db',
                    help='A JSON-file containing the schedule.')

PARSER.add_argument('--debug', dest='debug', default=False,
                    const=True, nargs="?",
                    help='A JSON-file containing the schedule.')

PARSER.add_argument('--create', dest='create', default=False, const=True,
                    nargs="?", help='Creates a new database. DELETES ALL DATA!!')

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
# # Setup Flask, switch_manager, config
# ######################################

SCHEDULE_FILE = ARGS.schedule_file
URL_PREFIX = '/api'

if ARGS.create:
    create_db(SCHEDULE_FILE)

SWITCH_MODEL = PiSwitchModel(SCHEDULE_FILE)
SWITCH_MANAGER = SwitchManager(SWITCH_MODEL)

APP = Flask(__name__)
API = Api(APP)

# ######################################
# # flask_restful:
# ######################################

PINS_SCHEMA = PinSchema(many=True)
PIN_SCHEMA  = PinSchema(many=False)

SEQUENCES_SCHEMA = SequenceSchema(many=True)
SEQUENCE_SCHEMA  = SequenceSchema(many=False)

# ––––––––––––––––––––––––––––––––––––––
# Pins
kwargs_pins = {
    'schema':       PINS_SCHEMA,
    'getter_func':  SWITCH_MODEL.get_pins,
    'setter_func':  SWITCH_MODEL.set_pin,
    'delete_func':  SWITCH_MODEL.delete_pin
    }

API.add_resource(ManyRessource, URL_PREFIX + '/pins', endpoint='pins',
                 resource_class_kwargs=kwargs_pins)
kwargs_pin = {
    'schema':       PIN_SCHEMA,
    'getter_func':  SWITCH_MODEL.get_pin,
    'setter_func':  SWITCH_MODEL.set_pin,
    'delete_func':  SWITCH_MODEL.delete_pin
    }

API.add_resource(SingleResource, URL_PREFIX + '/pins/<int:pin_id>', endpoint='pin',
                 resource_class_kwargs=kwargs_pin)

# ––––––––––––––––––––––––––––––––––––––
# Sequences
kwargs_sequences = {
    'schema':       SEQUENCES_SCHEMA,
    'getter_func':  SWITCH_MODEL.get_sequences_for_pin,
    'setter_func':  SWITCH_MODEL.set_sequence,
    'delete_func':  SWITCH_MODEL.delete_sequence
    }
sequences_url = URL_PREFIX + '/pins/<int:pin_id>/sequences'
API.add_resource(ManyRessource, sequences_url, endpoint='pins_sequences',
                 resource_class_kwargs=kwargs_sequences)

kwargs_sequences['getter_func'] = SWITCH_MODEL.get_sequences

API.add_resource(ManyRessource, URL_PREFIX + '/sequences', endpoint='sequences',
                 resource_class_kwargs=kwargs_sequences)

kwargs_sequence = kwargs_sequences
kwargs_sequence['schema'] = SEQUENCE_SCHEMA
kwargs_sequence['getter_func'] = SWITCH_MODEL.get_sequence

API.add_resource(SingleResource, URL_PREFIX + '/sequences/<int:sequence_id>',
                 endpoint='sequence', resource_class_kwargs=kwargs_sequence)

# ––––––––––––––––––––––––––––––––––––––
# Time

if __name__ == '__main__':
    SWITCH_MANAGER.start()
    try:
        APP.run(debug=ARGS.debug)
    finally:
        SWITCH_MANAGER.stop()
        LOGGER.info("############# END OF LOG #############\n")
