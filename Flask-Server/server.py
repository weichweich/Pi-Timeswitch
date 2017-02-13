# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_restful import Api

from time_switch.switch_manager import SwitchManager
from time_switch.model import create_db, PiSwitchModel
from schema import PinSchema, SequenceSchema
from rest_model_adapter import ManyRessource, SingleResource

import argparse
import logging

# ######################################
# # parsing commandline args
# ######################################

parser = argparse.ArgumentParser(description='Timeswitch for the\
 GPIOs of an Raspberry Pi with a webinterface.')
parser.add_argument('--file', dest='schedule_file', metavar='file',
                    type=str, default='gpio_time.db',
                    help='A JSON-file containing the schedule.')

parser.add_argument('--debug', dest='debug', default=False,
                    const=True, nargs="?",
                    help='A JSON-file containing the schedule.')

parser.add_argument('--create', dest='create', default=False, const=True,
                    nargs="?", help='Creates a new database. DELETES ALL DATA!!')

args = parser.parse_args()

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
console = logging.StreamHandler()

if args.debug:
    console.setLevel(logging.DEBUG)
else:
    console.setLevel(logging.INFO)

# set a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s:%(name)-8s:%(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

logger = logging.getLogger("MAIN")

# ######################################
# # Setup Flask, switch_manager, config, auth
# ######################################

schedule_file = args.schedule_file
URL_PREFIX = '/api'

if args.create:
    create_db(schedule_file)

switch_model = PiSwitchModel(schedule_file)
switch_manager = SwitchManager(switch_model)

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'secret key here'

# ######################################
# # flask_restful:
# ######################################

# ––––––––––––––––––––––––––––––––––––––
# Pins
kwargs_pins = {
    'decorators':   [],
    'schema':       PinSchema,
    'getter_func':  switch_model.get_pins,
    'setter_func':  switch_model.set_pin,
    'delete_func':  switch_model.delete_pin
    }

api.add_resource(ManyRessource, URL_PREFIX + '/pins', endpoint='pins',
                 resource_class_kwargs=kwargs_pins)
kwargs_pin = {
    'decorators':   [],
    'schema':       PinSchema,
    'getter_func':  switch_model.get_pin,
    'setter_func':  switch_model.set_pin,
    'delete_func':  switch_model.delete_pin
    }

api.add_resource(SingleResource, URL_PREFIX + '/pins/<int:pin_id>', endpoint='pin',
                 resource_class_kwargs=kwargs_pin)

# ––––––––––––––––––––––––––––––––––––––
# Sequences
kwargs_sequences = {
    'decorators':   [],
    'schema':       SequenceSchema,
    'getter_func':  switch_model.get_sequences_for_pin,
    'setter_func':  switch_model.set_sequence,
    'delete_func':  switch_model.delete_sequence
    }
sequences_url = URL_PREFIX + '/pins/<int:pin_id>/sequences'
api.add_resource(ManyRessource, sequences_url, endpoint='pins_sequences',
                 resource_class_kwargs=kwargs_sequences)

kwargs_sequences['getter_func'] = switch_model.get_sequences

api.add_resource(ManyRessource, URL_PREFIX + '/sequences', endpoint='sequences',
                 resource_class_kwargs=kwargs_sequences)

kwargs_sequences['getter_func'] = switch_model.get_sequence

api.add_resource(SingleResource, URL_PREFIX + '/sequences/<int:sequence_id>',
                 endpoint='sequence', resource_class_kwargs=kwargs_sequences)

# ––––––––––––––––––––––––––––––––––––––
# Time

if __name__ == '__main__':
    switch_manager.start()
    try:
        app.run(debug=args.debug)
    finally:
        switch_manager.stop()
        logger.info("############# END OF LOG #############\n")
