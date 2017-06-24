# -*- coding: utf-8 -*-

import json
import argparse
import logging
import os
import sys

from flask import Flask, make_response
from flask_restful import Api

from timeswitch.switch.manager import SwitchManager
from timeswitch.switch.model import create_db as time_db_init, SwitchModel
from timeswitch.switch.schema import PinSchema, SequenceSchema
from timeswitch.rest_model_adapter import ManyRessource, SingleResource
import timeswitch.auth as auth
from timeswitch.auth.model import create_db as auth_db_init
from timeswitch.auth.resource import UsersResource, UserResource, LoginResource

# ######################################
# # parsing commandline args
# ######################################

PARSER = argparse.ArgumentParser(description='Timeswitch for the\
 GPIOs of an Raspberry Pi with a webinterface.')
PARSER.add_argument('-f', '--file', dest='schedule_file', metavar='file',
                    type=str, required=True,
                    help='A JSON-file containing the schedule.')

PARSER.add_argument('--debug', action='store_true',
                    help='A JSON-file containing the schedule.')

PARSER.add_argument('--create', dest='create', action='store_true',
                    help='Creates a new database. DELETES ALL DATA!!')

PARSER.add_argument('--manager', dest='manager', action='store_true',
                    help='Start the manager which switches the GPIOs at specified times.')

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
console = logging.StreamHandler()

if ARGS.debug:
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
app.config['SQL_FILE'] = ARGS.schedule_file

if ARGS.create:
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

def main():
    switch_manager = None
    if ARGS.manager:
        switch_manager = SwitchManager(switch_model)
        switch_manager.start()

    try:
        app.run(debug=ARGS.debug)
    finally:
        if ARGS.manager:
            switch_manager.stop()
    logger.info("############# END OF LOG #############\n")

if __name__ == '__main__':
    main()
