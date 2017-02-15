# -*- coding: utf-8 -*-

from flask import Flask, g
from flask_restful import Api

from time_switch.switch_manager import SwitchManager
from time_switch.model import create_db as time_db_init, PiSwitchModel
from time_switch.schema import PinSchema, SequenceSchema
from rest_model_adapter import ManyRessource, SingleResource
from auth import create_db as auth_db_init, dec_auth
from auth.resource import UsersResource, UserResource

import argparse
import logging
import os

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

URL_PREFIX = '/api'


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'secret'
app.config['SQL_FILE'] = args.schedule_file

if args.create:
	if os.path.exists(app.config['SQL_FILE']):
		os.remove(app.config['SQL_FILE'])
	with app.app_context():
		auth_db_init()
		time_db_init()

switch_model = PiSwitchModel(app.config['SQL_FILE'])
switch_manager = SwitchManager(switch_model)

# ######################################
# # flask_restful:
# ######################################

# ––––––––––––––––––––––––––––––––––––––
# Pins
kwargs_pins = {
	'decorators':   [dec_auth],
	'schema':       PinSchema,
	'getter_func':  switch_model.get_pins,
	'setter_func':  switch_model.set_pin,
	'delete_func':  switch_model.delete_pin
	}

api.add_resource(ManyRessource, URL_PREFIX + '/pins', endpoint='pins',
				 resource_class_kwargs=kwargs_pins)
kwargs_pin = {
	'decorators':   [dec_auth],
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
	'decorators':   [dec_auth],
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
# User

api.add_resource(UsersResource, URL_PREFIX + '/users',
				 endpoint='users')

api.add_resource(UserResource, URL_PREFIX + '/users/<string:user_name>',
				 endpoint='user')

if __name__ == '__main__':
	switch_manager.start()
	try:
		app.run(debug=args.debug)
	finally:
		switch_manager.stop()
		logger.info("############# END OF LOG #############\n")
