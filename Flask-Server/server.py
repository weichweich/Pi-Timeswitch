# -*- coding: utf-8 -*-

from flask import Flask, g, make_response
from flask_restful import Api

from time_switch.model import create_db as time_db_init, SwitchModel
from time_switch.schema import PinSchema, SequenceSchema
from rest_model_adapter import ManyRessource, SingleResource
import auth
from auth.model import create_db as auth_db_init
from auth.resource import UsersResource, UserResource, LoginResource

import json
import argparse
import logging
import os
import sys

# ######################################
# # parsing commandline args
# ######################################

parser = argparse.ArgumentParser(description='Timeswitch for the\
 GPIOs of an Raspberry Pi with a webinterface.')
parser.add_argument('-f', '--file', dest='schedule_file', metavar='file',
                    type=str, required=True,
                    help='A JSON-file containing the schedule.')

parser.add_argument('--debug', action='store_true',
                    help='A JSON-file containing the schedule.')

parser.add_argument('--create', dest='create', action='store_true',
                    help='Creates a new database. DELETES ALL DATA!!')

parser.add_argument('--manager', dest='manager', action='store_true',
                    help='Start the manager which switches the GPIOs at specified times.')

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
api = Api(app, default_mediatype='application/vnd.api+json')
app.config['SECRET_KEY'] = 'secret'
app.config['SQL_FILE'] = args.schedule_file

if args.create:
	if os.path.exists(app.config['SQL_FILE']):
		os.remove(app.config['SQL_FILE'])
	with app.app_context():
		auth_db_init()
		time_db_init()
	sys.exit(0)

switch_model = SwitchModel(app.config['SQL_FILE'])

# ######################################
# # flask_restful:
# ######################################

@api.representation('application/vnd.api+json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp

# ––––––––––––––––––––––––––––––––––––––
# Pins
kwargs_pins = {
	'decorators':   [auth.dec_auth],
	'schema':       PinSchema,
	'getter_func':  switch_model.get_pins,
	'setter_func':  switch_model.set_pin,
	'delete_func':  switch_model.delete_pin
	}

api.add_resource(ManyRessource, URL_PREFIX + '/pins', endpoint='pins',
				 resource_class_kwargs=kwargs_pins)
kwargs_pin = {
	'decorators':   [auth.dec_auth],
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
	'decorators':   [auth.dec_auth],
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

api.add_resource(UserResource, URL_PREFIX + '/users/<int:user_id>',
				 endpoint='user')

# ––––––––––––––––––––––––––––––––––––––
# Login
api.add_resource(LoginResource, URL_PREFIX + "/login", endpoint='login')

if __name__ == '__main__':
	switch_manager = None
	if (args.manager):
		switch_manager = SwitchManager(switch_model)
		switch_manager.start()

	try:
		app.run(debug=args.debug)
	finally:
		if (args.manager):
			switch_manager.stop()
		logger.info("############# END OF LOG #############\n")
