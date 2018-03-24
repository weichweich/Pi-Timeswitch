import json

from flask import make_response
from flask_restful import Api

import timeswitch.auth as auth
from timeswitch.auth.resource import LoginResource, UserResource, UsersResource
from timeswitch.rest_model_adapter import ManyRessource, SingleResource
from timeswitch.switch.schema import PinSchema, SequenceSchema


def setup_api(app, model, url_prefix='/api'):
    api = Api(app, default_mediatype='application/vnd.api+json')

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
        'getter_func':  model.get_pins,
        'setter_func':  model.set_pin,
        'delete_func':  model.delete_pin
        }

    api.add_resource(ManyRessource, url_prefix + '/pins', endpoint='pins',
                     resource_class_kwargs=kwargs_pins)
    kwargs_pin = {
        'decorators':   [auth.dec_auth],
        'schema':       PinSchema,
        'getter_func':  model.get_pin,
        'setter_func':  model.set_pin,
        'delete_func':  model.delete_pin
        }

    api.add_resource(SingleResource, url_prefix + '/pins/<int:pin_id>', endpoint='pin',
                     resource_class_kwargs=kwargs_pin)

    # ––––––––––––––––––––––––––––––––––––––
    # Sequences
    kwargs_sequences = {
        'decorators':   [auth.dec_auth],
        'schema':       SequenceSchema,
        'getter_func':  model.get_sequences_for_pin,
        'setter_func':  model.set_sequence,
        'delete_func':  model.delete_sequence
        }
    sequences_url = url_prefix + '/pins/<int:pin_id>/sequences'
    api.add_resource(ManyRessource, sequences_url, endpoint='pins_sequences',
                     resource_class_kwargs=kwargs_sequences)

    kwargs_sequences['getter_func'] = model.get_sequences

    api.add_resource(ManyRessource, url_prefix + '/sequences', endpoint='sequences',
                     resource_class_kwargs=kwargs_sequences)

    kwargs_sequences['getter_func'] = model.get_sequence

    api.add_resource(SingleResource, url_prefix + '/sequences/<int:sequence_id>',
                     endpoint='sequence', resource_class_kwargs=kwargs_sequences)

    # ––––––––––––––––––––––––––––––––––––––
    # User
    api.add_resource(UsersResource, url_prefix + '/users',
                     endpoint='users')

    api.add_resource(UserResource, url_prefix + '/users/<int:user_id>',
                     endpoint='user')

    # ––––––––––––––––––––––––––––––––––––––
    # Login
    api.add_resource(LoginResource, url_prefix + "/login", endpoint='login')

    return api